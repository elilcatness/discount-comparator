from sqlalchemy import Column, Integer, String, ForeignKey

from ..db.db_session import SQLAlchemyBase


class Product(SQLAlchemyBase):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    price = Column(Integer)
    img = Column(String)
    market_id = Column(Integer, ForeignKey('markets.id'))