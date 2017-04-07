import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    google_id = Column(String(80), nullable=False, unique=True)
    items = relationship("Item")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    items = relationship("Item")

    @property
    def serialize(self):
        """ JSON serializer method """
        return {
            'id': self.id,
            'name': self.name,
            'Items' : [item.serialize for item in self.items]
        }

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    description = Column(String(2000))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """ JSON serializer """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cat_id': self.category_id
        }

if __name__ == '__main__':
    engine = create_engine('sqlite:///database.sqlite')
    Base.metadata.create_all(engine)