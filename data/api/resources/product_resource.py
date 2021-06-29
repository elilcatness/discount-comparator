from flask_restful import Resource, abort

from data.db import db_session
from data.models.market import Market
from data.models.product import Product
from data.api.parsers.product_parsers import ProductParser


class BasicResource(Resource):
    parsers = []


class ProductResource(BasicResource):
    def get(self):
        args = ProductParser().parse_args()
        with db_session.create_session() as session:
            query = ["(args['price_from'] <= Product.price <= args['price_to'])"]
            if args['title']:
                query.append("(Product.title.like('%' + args['title']) + '%')")
            if args['market']:
                query.append("(Product.market.name == args['market'])")
            print(' and '.join(query))
            result = session.query(Product).filter(exec(' and '.join(query))).first()
            return result.to_dict()


class ProductListResource(BasicResource):
    pass