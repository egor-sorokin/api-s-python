from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    picture = Column(String)
    description = Column(String)
    price = Column(String)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'picture': self.picture,
            'price': self.price,
            'description': self.description
        }


engine = create_engine('sqlite:///bargainMart.db')

Base.metadata.create_all(engine)
