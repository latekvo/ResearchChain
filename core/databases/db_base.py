import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine(
    "postgresql://postgres:zaq12wsx@localhost:5432/postgres"
)  # this string needs to be replaced

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.CRITICAL)


class Base(DeclarativeBase):
    pass


def db_init():
    Base.metadata.create_all(bind=engine)
