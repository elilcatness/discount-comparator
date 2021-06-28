import os

from data.db import db_session
from data.parsers.dixy import DixyParser
from data.parsers.pyaterochka import PyaterochkaParser
from data.parsers.magnit import MagnitParser
from data.models.product import Product
from data.models.market import Market


def main():
    with db_session.create_session() as session:
        dixy_region = 'Ленинградская область'
        dixy_market = session.query(Market).filter(
            (Market.name == 'Дикси') and (Market.region == dixy_region)).first()
        products = [pr.to_dict() for pr in dixy_market.products]
        dixy = DixyParser(dixy_region, products)


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'db', 'base.db'))
    main()