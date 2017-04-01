from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    restaurant_name = Column(String)
    restaurant_address = Column(Integer)
    restaurant_image = Column(Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'restaurant_name': self.restaurant_name,
            'restaurant_address': self.restaurant_address,
            'restaurant_image': self.restaurant_image
        }


engine = create_engine('sqlite:///restaurants.db')

Base.metadata.create_all(engine)
