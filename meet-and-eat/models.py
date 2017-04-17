import string
import random

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    pass


class Request(User):
    pass


class Proposal(Request):
    pass


class MealDate(Base):
    pass


engine = create_engine('sqlite:///meetandeat.db')
Base.metadata.create_all(engine)
