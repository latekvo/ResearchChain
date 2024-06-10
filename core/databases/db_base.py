from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite://", echo=True)


class Base(DeclarativeBase):
    pass


def db_init():
    Base.metadata.create_all(engine)
