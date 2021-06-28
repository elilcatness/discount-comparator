from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relation

from ..db.db_session import SQLAlchemyBase


class Market(SQLAlchemyBase):
    __tablename__ = 'markets'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    region = Column(String)
    products = relation('Product', overlaps='market')