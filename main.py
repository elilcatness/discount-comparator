from flask import Flask
from flask_restful import Api
import os

from data.db import db_session
from data.parsers.dixy import Dixy
from data.parsers.pyaterochka import Pyaterochka
from data.parsers.magnit import Magnit
from data.models.product import Product
from data.models.market import Market
from data.api.resources.product import ProductResource, ProductListResource
from data.api.resources.market import MarketListResource

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)
api.add_resource(ProductResource, '/api/product')
api.add_resource(ProductListResource, '/api/products')
api.add_resource(MarketListResource, '/api/markets')


def main():
    with db_session.create_session() as session:
        market = session.query(Dixy).first()


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'db', 'base.db'))
    # main()
    app.run()