from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

SQLAlchemyBase = declarative_base()
__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return
    db_file = db_file.strip()
    if not db_file:
        return
    engine = create_engine(f'sqlite:///{db_file}?check_same_thread=False', poolclass=NullPool, echo=False)
    __factory = sessionmaker(bind=engine)
    from . import __all_models
    SQLAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()