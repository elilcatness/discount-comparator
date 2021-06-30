from flask import Flask
from flask_restful import Api
import os

from data.db import db_session
from data.parsers.dixy import Dixy
from data.parsers.pyaterochka import PyaterochkaParser
from data.parsers.magnit import Magnit
from data.models.product import Product
from data.models.market import Market
from data.api.resources.product_resource import ProductResource, ProductListResource

app = Flask(__name__)
api = Api(app)
api.add_resource(ProductResource, '/api/product')
api.add_resource(ProductListResource, '/api/products')


def main():
    with db_session.create_session() as session:
        dixy = session.query(Dixy).get(4)
        print(dixy.id)


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'db', 'base.db'))
    # main()
    app.run()