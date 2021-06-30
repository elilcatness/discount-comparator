from flask_restful.reqparse import RequestParser


class MarketParser(RequestParser):
    def __init__(self):
        super(MarketParser, self).__init__()
        self.add_argument('name', type=str, required=True)
        self.add_argument('region', type=str, required=True)