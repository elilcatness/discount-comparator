from flask_restful.reqparse import RequestParser


class ProductParser(RequestParser):
    def __init__(self):
        super(ProductParser, self).__init__()
        self.add_argument('title', required=False)
        self.add_argument('market', required=False)
        self.add_argument('price_from', default=0)
        self.add_argument('price_to', default=float('inf'))