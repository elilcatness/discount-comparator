import logging
import time
from datetime import timedelta

from humanize import precisedelta
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from data.db import db_session
from data.models.product import Product
from data.parsers.commonParser import CommonParser
from data.exceptions import InvalidRegionError


class Dixy(CommonParser):
    """Class that consists of products data of Dixy market in particular region and updates them"""

    url: str = 'https://dixy.ru/catalog/'
    interval: int = 3600

    def __init__(self, region: str = 'Санкт-Петербург'):
        super(Dixy, self).__init__(region)

    def select_region(self):
        error_msg = f'Failed to find {self.region} in region buttons [IN {self}]'

        self.driver.get(self.url)
        region_select_menu = self.driver.find_element_by_class_name('icon-arrow-down')
        if not region_select_menu:
            return logging.error(message=f'Failed to get region select menu [IN {self}]')
        region_select_menu.click()
        region_buttons = self.driver.find_elements_by_xpath('//div[@class="simplebar-content"]/ul//li/a')
        if not region_buttons:
            logging.error(message=error_msg)
            raise InvalidRegionError(error_msg)
        try:
            region_button = list(filter(lambda reg: reg.text.lower() == self.region.lower(),
                                        region_buttons))[0]
        except IndexError:
            logging.error(error_msg)
            raise InvalidRegionError(error_msg)
        region_button.click()
        print('\nSET REGION\n')
        return True

    def scroll_to_bottom(self, tag: str, class_: str):
        elem = True
        been_toggled = False
        while elem:
            try:
                elem = self.driver.find_element_by_xpath(f'//{tag}[@class="{class_}"]')
            except NoSuchElementException:
                elem = None
            if not elem and not been_toggled:
                return logging.warning(message='Failed to scroll to bottom', market=self)
            elif elem:
                been_toggled = True
                try:
                    elem.click()
                except ElementClickInterceptedException:
                    print('I AM STUCK')
                    continue

    def update_data(self, init_call=False):
        print('\nSTARTED UPDATING DATA\n')
        if not init_call:
            self.driver.refresh()

        self.scroll_to_bottom('a', 'btn view-more')

        checked = []
        idx_to = len(self.products)

        session = db_session.create_session()

        products = self.driver.find_elements_by_class_name('dixyCatalogItem ')
        for product in products:
            try:
                pic_block = product.find_element_by_class_name('dixyModal__pic'
                                                               ).find_element_by_tag_name('img')
                title = pic_block.get_attribute('alt').replace('\xa0', ' ')
                try:
                    price = int(product.find_element_by_xpath('.//p[@itemprop="price"]'
                                                              ).get_attribute('content'))
                except ValueError:
                    continue
                checked = self.merge_product(title, price, checked)
                prod = Product(title=title, price=price, img=pic_block.get_attribute('src'))
                session.add(prod)
                session.commit()
                self.products.append(prod)
                session.merge(self)
                session.commit()
            except NoSuchElementException as e:
                logging.warning(msg=f'{e.msg} [IN {self}]')

        for i in range(idx_to):
            if i not in checked:
                session.delete(self.products.pop(i))

        session.commit()
        session.close()

        self.set_refresh_process()

    def __repr__(self):
        return f'Дикси. {self.region[0].upper() + self.region[1:]}'


if __name__ == '__main__':
    start_time = time.time()
    dixy = Dixy('Ленинградская область')
    print('\n'.join([', '.join([f'{key}: {val}' for key, val in [item for item in product.items()]])
                     for product in dixy.get_data()]))
    seconds, microseconds = map(int, '{0:.2f}'.format(time.time() - start_time).split('.'))
    print(f'Time passed: {precisedelta(timedelta(seconds=seconds, microseconds=microseconds))}')
