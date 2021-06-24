import logging

from selenium.common.exceptions import NoSuchElementException

from .commonParser import CommonParser


class PyaterochkaParser(CommonParser):
    """Class that consists of products data of Pyterochka market in particular address and updates them"""

    url: str = ''

    def __init__(self, address: str):
        super(PyaterochkaParser, self).__init__(address)