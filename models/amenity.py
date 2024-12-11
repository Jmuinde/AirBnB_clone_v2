#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os

class Amenity(BaseModel, Base):
	"""Class amenity tied to the place """
	__tablename__ = 'amenities'
	if os.getenv('HBNB_TYPE_STORAGE') == 'db':
		name = Column(String(128), nullable = False)
	
	else:
	
		name = ""
