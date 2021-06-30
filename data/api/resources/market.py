from typing import Union
from flask import jsonify
from flask_restful import Resource

from data.db import db_session
from data.models.market import Market
from data.parsers.dixy import Dixy
from data.parsers.magnit import Magnit
from data.parsers.pyaterochka import Pyaterochka


class BasicResource(Resource):
    markets: list[Union[Dixy, Magnit, Pyaterochka]] = []

    def __init__(self):
        self.session = db_session.create_session()
        for name in {m.name for m in self.session.query(Market).all()}:
            self.markets.extend(self.session.query(eval(name)).all())


class MarketListResource(BasicResource):
    def get(self):
        return jsonify([market.to_dict() for market in self.markets])