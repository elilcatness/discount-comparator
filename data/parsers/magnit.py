import logging
import time

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    StaleElementReferenceException

from .commonParser import CommonParser


class MagnitParser(CommonParser):
    url = 'https://magnit.ru/promo/'

    def __init__(self, region: str, data_to_load: list = None):
        super(MagnitParser, self).__init__(region, data_to_load)

    def select_region(self):
        button_load_interval = 30
        result_load_interval = 5

        self.driver.get(self.url)

        try:
            age_button = self.driver.find_element_by_xpath('//button[@class="g-button"]')
            age_button.click()
            start_time = time.time()
            region_button = self.driver.find_element_by_xpath(
                '//button[@class="g-button g-button_filter '
                'js-geo-another"]')
            while True:
                try:
                    region_button.click()
                    break
                except ElementNotInteractableException:
                    if time.time() - start_time > button_load_interval:
                        return logging.error(
                            msg=f'Failed to select region by clicking the button [IN {self}]')
        except NoSuchElementException as e:
            return logging.error(msg=f'{e.msg} [IN {self}]')

        field = self.driver.find_element_by_xpath('//input[@name="citySearch"]')
        field.clear()
        field.send_keys(self.region)

        start_time = time.time()
        while True:
            try:
                link = self.driver.find_element_by_xpath('//a[@class="city-search__link "]')
                break
            except NoSuchElementException:
                if time.time() - start_time > result_load_interval:
                    return logging.error(msg=f'Failed to find region [IN {self}]')
        link.click()
        loaded = False
        time.sleep(result_load_interval)
        start_time = time.time()
        while not loaded:
            loaded = self.driver.execute_script('return document.readyState;') == 'complete'
            if time.time() - start_time > button_load_interval:
                return logging.error(f'Failed to load page [IN {self}]')
        return True

    def update_data(self, init_call: bool = False):
        if not init_call:
            self.driver.refresh()

        scroll_height = 0
        scroll_step = 200
        scroll_limit = self.driver.execute_script('return document.body.scrollHeight;')

        idx_to = len(self.data)
        checked = []

        products = self.driver.find_elements_by_xpath('//div[@class="сatalogue__main js-promo-container"]'
                                                      '/a')
        for product in products:
            if scroll_height < scroll_limit:
                scroll_height += scroll_step
                self.driver.execute_script(f'window.scrollTo(0, {scroll_height});')
            try:
                img_block = product.find_element_by_xpath('./div[@class="card-sale__col '
                                                          'card-sale__col_img"]'
                                                          '/picture/img')
                title = img_block.get_attribute('alt')
                try:
                    price = int(product.find_element_by_xpath('.//span[@class="label__price-'
                                                              'integer"]').text)
                except ValueError:
                    continue
                try:
                    idx = self.data.index(list(filter(lambda prod: prod['title'] == title,
                                                      self.data))[0])
                    if self.data[idx]['price'] == price:
                        checked.append(idx)
                except IndexError:
                    pass
                self.data.append({'title': title,
                                  'price': price,
                                  'img': img_block.get_attribute('src')})
                print(self.data[-1])
            except (NoSuchElementException, StaleElementReferenceException) as e:
                logging.warning(msg=f'{e.msg} [IN {self}]')

        for i in range(idx_to):
            if i in checked:
                self.data.pop(i)

    def __repr__(self):
        return f'Магнит. {self.region}'
