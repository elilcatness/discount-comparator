import logging
import time

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import Chrome

from .commonParser import CommonParser


class MagnitParser(CommonParser):
    url = 'https://magnit.ru/promo/'

    def __init__(self, region: str):
        super(MagnitParser, self).__init__(region)

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
        return True

    def __repr__(self):
        return f'Магнит. {self.region}'
