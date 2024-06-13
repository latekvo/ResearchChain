import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("postgresql://postgres:pass@postgres:5432/postgres")

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.CRITICAL)


class Base(DeclarativeBase):
    pass


def db_init():
    connection = engine.connect()
    Base.metadata.create_all(engine)
