from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relation
from sqlalchemy_serializer import SerializerMixin

from ..db.db_session import SQLAlchemyBase


class Market(SQLAlchemyBase, SerializerMixin):
    __tablename__ = 'markets'

    serialize_only = ('id', 'products.id', 'products.title',
                      'products.price', 'products.img', 'region')

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    region = Column(String)
    products = relation('Product', overlaps='market')