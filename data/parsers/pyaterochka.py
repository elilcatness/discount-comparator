import logging
import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Chrome

from .commonParser import CommonParser


class PyaterochkaParser(CommonParser):
    """Class that consists of products data of Pyterochka market in particular address and updates them"""

    url: str = 'https://5ka.ru/special_offers/'

    def __init__(self, region: str, data_to_load: list = None):
        super(PyaterochkaParser, self).__init__(region, data_to_load)

    def select_region(self):
        search_time = 5

        self.driver.get(self.url)
        self.driver.execute_script(
            'document.getElementsByClassName("location__select-city")[0].click();')

        field = self.driver.find_element_by_class_name('search__input')
        field.send_keys(self.region)

        time.sleep(search_time)

        results = self.driver.find_elements_by_xpath('.//div[@class="suggestions"]/ul//li/div')
        if not results:
            logging.error(msg=f'Failed to find region [IN {self}]')
        self.region = results[0].text
        results[0].click()
        return True

    def update_data(self, init_call=False):
        self.driver: Chrome

        self.driver.refresh()

        scroll_height = 0
        scroll_step = 200
        scroll_limit = self.driver.execute_script('return document.body.scrollHeight;')

        idx_to = len(self.data)
        checked = []

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
                try:
                    idx = self.data.index(list(filter(lambda prod: prod['title'] == title,
                                                      self.data))[0])
                    if self.data[idx]['price'] == price:
                        checked.append(idx)
                except IndexError:
                    pass
                img = product.find_element_by_xpath('.//img[@class="sale-card__img"]').get_attribute('src')
                self.data.append({'title': title,
                                  'price': price,
                                  'img': img})
                print(self.data[-1])
            except (NoSuchElementException, StaleElementReferenceException) as e:
                logging.warning(msg=f'{e.msg} [IN {self}]')

        for i in range(idx_to):
            if i in checked:
                self.data.pop(i)

    def __repr__(self):
        return f'Пятёрочка. {self.region}'
