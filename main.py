import os

from data.db import db_session
from data.parsers.dixy import DixyParser

from data.parsers.magnit import MagnitParser
from data.models.product import Product
from data.models.market import Market


def main():
    with db_session.create_session() as session:
        region = 'Отрадное, Ленинградская область'
        magnit_data = [prod.to_dict() for prod in session.query(Market).filter(
            (Market.name == 'Магнит') and (Market.region == region)).first().products]
        magnit = MagnitParser('Отрадное, Ленинградская область', data_to_load=magnit_data)


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'db', 'base.db'))
    main()