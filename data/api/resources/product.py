from flask import jsonify
from flask_restful import Resource

from data.db import db_session
from data.models.product import Product
from data.api.parsers.product import ProductParser


class BasicResource(Resource):
    @staticmethod
    def get_query():
        args = ProductParser().parse_args()
        with db_session.create_session() as session:
            query = session.query(Product).filter(args['price_from'] <= Product.price
                                                  ).filter(Product.price >= args['price_to'])
            if args['title']:
                query = query.filter(Product.title.like(f"%{args['title']}%"))
            if args['market']:
                query = query.filter(Product.market.name == args['market'])
            return query


class ProductResource(BasicResource):
    def get(self):
        result = self.get_query().first()
        return jsonify(result.to_dict() if result else [])


class ProductListResource(BasicResource):
    def get(self):
        result = self.get_query().all()
        return jsonify([res.to_dict() for res in result] if result else [])