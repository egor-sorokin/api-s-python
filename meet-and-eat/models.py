import string
import random

from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, index=True)
    password_hash = Column(String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
        }


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    meal_type = Column(String, nullable=False, index=True)
    location_string = Column(String, nullable=False)
    latitude = Column(String(10))
    longitude = Column(String(10))
    meal_time = Column(String(20), nullable=False)
    filled = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'meal_type': self.meal_type,
            'location_string': self.location_string,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'meal_time': self.meal_time,
            'filled': self.filled,
            'user_id': self.user_id
        }


class Proposal(Base):
    __tablename__ = 'proposal'

    id = Column(Integer, primary_key=True)
    user_proposed_to = Column(String)
    user_proposed_from = Column(String)
    filled = Column(String)
    request_id = Column(String, ForeignKey('request.id'))
    relationship(Request)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_proposed_to': self.user_proposed_to,
            'user_proposed_from': self.user_proposed_from,
            'filled': self.filled,
            'request_id': self.request_id
        }


class MealDate(Base):
    __tablename__ = 'mealdate'

    id = Column(Integer, primary_key=True)
    user_first = Column(String)
    user_second = Column(String)
    restaurant_name = Column(String(100), nullable=False)
    restaurant_address = Column(String)
    restaurant_picture = Column(String)
    meal_time = Column(String, nullable=False, index=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_first': self.user_first,
            'user_second': self.user_second,
            'restaurant_name': self.restaurant_name,
            'restaurant_address': self.restaurant_address,
            'restaurant_picture': self.restaurant_picture,
            'meal_time': self.meal_time
        }


engine = create_engine('sqlite:///meetandeat.db')
Base.metadata.create_all(engine)
