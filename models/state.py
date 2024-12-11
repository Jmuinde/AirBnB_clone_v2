#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import os

class State(BaseModel, Base):
	""" State class """
	__tablename__ = 'states'
	if os.getenv('HBNB_TYPE_STORAGE') == 'db':
		name = Column(String(128), nullable=False)
		cities = relationship('City', cascade='all, delete, delete-orphan', backref='state')
	else:
		name = ""

		@property
		def cities(self):
			"""Returns the list of cities in each state"""
			from models.city import City
			from models import storage
			list_cities = []
			for city in storage.all(City).values():
				if city.state_id == self.id:
					list_cities.append(city)
			return list_cities
	
