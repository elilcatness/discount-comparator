from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relation

from ..db.db_session import SQLAlchemyBase


class Product(SQLAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    serialize_only = ('title', 'price', 'img')

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String)
    price = Column(Integer)
    img = Column(String)
    market_id = Column(Integer, ForeignKey('markets.id'))
    market = relation('Market', foreign_keys=market_id)