import logging
import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Chrome

from data.parsers.commonParser import CommonParser
from data.db import db_session
from data.models.product import Product
from data.exceptions import InvalidRegionError


class Pyaterochka(CommonParser):
    """Class that consists of products data of Pyterochka market in particular address and updates them"""

    url: str = 'https://5ka.ru/special_offers/'

    def __init__(self, region: str, data_to_load: list = None):
        super(Pyaterochka, self).__init__(region, data_to_load)

    def select_region(self):
        error_msg = f'Failed to find region [IN {self}]'
        search_time = 5

        self.driver.get(self.url)
        self.driver.execute_script(
            'document.getElementsByClassName("location__select-city")[0].click();')

        field = self.driver.find_element_by_class_name('search__input')
        field.send_keys(self.region)

        time.sleep(search_time)

        results = self.driver.find_elements_by_xpath('.//div[@class="suggestions"]/ul//li/div')
        if not results:
            logging.error(msg=error_msg)
            raise InvalidRegionError(error_msg)
        self.region = results[0].text
        results[0].click()
        return True

    def update_data(self, init_call=False):
        self.driver: Chrome

        self.driver.refresh()

        scroll_height = 0
        scroll_step = 200
        scroll_limit = self.driver.execute_script('return document.body.scrollHeight;')

        idx_to = len(self.products)
        checked = []

        session = db_session.create_session()

        products = self.driver.find_elements_by_xpath('//ul[@class="special-offers__offers"]'
                                                      '/a[@class="sale-card"]')
        for product in products:
            try:
                if scroll_height < scroll_limit:
                    scroll_height += scroll_step
                    self.driver.execute_script(f'window.scrollTo(0, {scroll_height});')
                title = product.find_element_by_xpath('.//p[@class="sale-card__title"]').text
                try:
                    price = int(product.find_element_by_xpath('.//span[@class="sale-card__price  '
                                                              'sale-card__price--new"]'
                                                              '/span').text.strip()[:-2])
                except ValueError:
                    continue
                checked = self.merge_product(title, price, checked)
                prod = Product(title=title, price=price,
                               img=product.find_element_by_xpath('.//img[@class="sale-card__img"]'
                                                                 ).get_attribute('src'))
                session.add(prod)
                session.commit()
                self.products.append(prod)
            except (NoSuchElementException, StaleElementReferenceException) as e:
                logging.warning(msg=f'{e.msg} [IN {self}]')

        for i in range(idx_to):
            if i not in checked:
                session.delete(self.products.pop(i))

        session.commit()
        session.close()

    def __repr__(self):
        return f'Пятёрочка. {self.region}'
