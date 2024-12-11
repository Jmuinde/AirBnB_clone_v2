#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import os

place_amenity = Table(
	'place_amenity',
	Base.metadata,
	Column('place_id', String(60), ForeignKey('places.id'), nullable = False, primary_key=True),
	Column('amenity_id', String(60), ForeignKey('amenities.id'), nullable= False, primary_key=True)
	)

""" Represents a many to many relationship table between Place and Amenity rows."""

class Place(BaseModel, Base):
	""" A place to stay """
	__tablename__ = 'places'
	if os.getenv('HBNB_TYPE_STORAGE') == 'db':
		city_id = Column(String(60), ForeignKey('cities.id'), nullable = False)
		user_id = Column(String(60), ForeignKey('users.id'), nullable = False)
		name = Column(String(128), nullable = False)
		description = Column(String(1024))
		number_rooms = Column(Integer, default = 0, nullable = False)
		number_bathrooms = Column(Integer, default = 0, nullable = False)
		max_guest = Column(Integer, default = 0, nullable = False)
		price_by_night = Column(Integer, default = 0, nullable = False)
		latitude = Column(Float)
		longitude = Column(Float)
		reviews = relationship('Review', cascade ='all, delete, delete-orphan', backref='place')
		amenities = relationship('Amenity', secondary=place_amenity, viewonly=False, backref='place_amenities')

	else:
		city_id = ""
		user_id = ""
		name = ""
		description = ""
		number_rooms = 0
		number_bathrooms = 0
		max_guest = 0
		price_by_night = 0
		latitude = 0.0
		longitude = 0.0
		amenity_ids = []
		
		@property
		def amenities(self):
			"""Returns the list of amenities available in the place"""
			from models import storage
			list_place_amenities = []
			for amenity in storage.all(Amenity).values():
				if amenity.id in self.amenity_ids:
					list_place_amenities.append(amenity)
			return list_place_amenities
			
		@amenities.setter
		def amenities(self, value):
			"""Adds an amenity to this place"""
			if type(value) is Amenity:
				if value.id not in self.amenity_ids:
					self.amenity_ids.append(value.id)
		@property
		def reviews(self):
			"""Returns a list of review instances releted to place"""
			from models import storage
			place_reviews = []
			for review in storage.all(Review).values():
				if review.place_id == self.id:
					place_reviews.append(review)
			return place_reviews
