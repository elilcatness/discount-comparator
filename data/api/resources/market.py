from flask import jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, abort

from data.api.parsers.market import MarketParser
from data.db import db_session
from data.exceptions import InvalidRegionError
from data.models.market import Market
from data.parsers.dixy import Dixy
from data.parsers.magnit import Magnit
from data.parsers.pyaterochka import Pyaterochka
from data.api.utils import UpdateThread


class BasicResource(Resource):
    def __init__(self):
        self.session = db_session.create_session()
        for name in {m.name for m in self.session.query(Market).all()}:
            for market in self.session.query(eval(name)).all():
                market.__init__()
                thread = UpdateThread(market)
                thread.start()


class MarketListResource(BasicResource):
    def get(self):
        return jsonify([market.to_dict() for market in self.session.query(Market).all()])

    # @jwt_required
    def post(self):
        args = MarketParser().parse_args()
        args['name'] = args['name'].lower().capitalize()
        try:
            cls = eval(args['name'])
        except NameError:
            return abort(400, message='Invalid market name')
        if self.session.query(Market).filter((Market.name == args['name'])
                                             and (Market.region == args['region'])).first():
            return abort(400, message='Market already exists')
        try:
            market = cls(region=args['region'])
        except InvalidRegionError:
            return abort(400, message='Invalid region for this market was passed')
        self.session.add(market)
        self.session.commit()
        thread = UpdateThread(market)
        thread.start()
        return jsonify({'message': 'OK'})