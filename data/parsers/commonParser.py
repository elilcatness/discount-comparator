import logging
import os
from threading import Timer

from selenium.webdriver import Chrome, ChromeOptions

from ..exceptions import InheritanceError
from ..models.market import Market


class CommonParser(Market):
    url: str = None
    interval: int = None

    def __init__(self, region: str, data_to_load: list = None):
        logging.basicConfig(filename=os.path.join('parser.log'),
                            format='%(asctime)s %(levelname)s '
                                   '%(name)s %(message)s',
                            encoding='utf-8')
        if not self.url:
            raise InheritanceError('Child class should have an url attribute')
        self.driver = None
        # self.update_driver()

        self.region = region
        # self.set_region(region)

        self.data = data_to_load if data_to_load else []

        self.refresh_thread = None
        self.update_data(init_call=True)

    def update_driver(self):
        if not getattr(self, 'driver', None):
            options = ChromeOptions()
            options.add_argument('--headless')
            self.driver = Chrome(executable_path=os.path.join('data', 'plugins', 'chromedriver.exe'),
                                 options=options)

    def close_driver(self):
        self.driver.close()

    def set_refresh_process(self):
        self.refresh_thread = Timer(self.interval, self.update_data)
        self.refresh_thread.start()

    def set_region(self, region: str):
        self.region = region
        self.select_region()

    def select_region(self):
        pass

    def merge_product(self, title: str, price: int, array: list):
        try:
            idx = self.products.index(list(filter(lambda prod: prod.title == title,
                                                  self.products))[0])
            if self.data[idx].price == price:
                array.append(idx)
        except IndexError:
            pass
        return array

    def update_data(self, init_call=False):
        pass

    def get_data(self):
        return self.data
