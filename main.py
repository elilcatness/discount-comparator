import os

from data.db import db_session
from data.parsers.dixy import DixyParser
from data.parsers.pyaterochka import PyaterochkaParser
from data.parsers.magnit import MagnitParser
from data.models.product import Product
from data.models.market import Market


def main():
    with db_session.create_session() as session:
        pass


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'db', 'base.db'))
    main()