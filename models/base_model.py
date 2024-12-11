#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
""" Moving from filestorage to dbstorage
"""

Base = declarative_base()

class BaseModel:
	id = Column(String(60), nullable = False, primary_key=True)
	created_at = Column(DateTime, nullable = False, default = datetime.utcnow())
	updated_at = Column(DateTime, nullable = False, default = datetime.utcnow())

	def __init__(self, *args, **kwargs):
		if not kwargs:
			self.id = str(uuid.uuid4())
			self.created_at = datetime.now()
			self.updated_at = datetime.now()

		else:
			for key, value in kwargs.items():
				if key != '__class__':
					if key in ('created_at', 'updated_at'):
						setattr(self, key, datetime.fromisoformat(value))
					else:
						setattr(self, key, value)
		# for os.getenv 'HBNB_TYPE_STORAGE' == 'db'
		if not hasattr(kwargs, 'id'):
			setattr(self, 'id', str(uuid.uuid4()))
		if not hasattr(kwargs, 'created_at'):
			setattr(self, 'created_at', datetime.now())
		if not hasattr(kwargs, 'updated_at'):
			setattr(self, 'updated_at', datetime.now())
				
	def __str__(self):
		cls = (str(type(self)).split('.')[-1]).split('\'')[0]
		return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

	def save(self):
		from models import storage
		self.updated_at = datetime.now()
		storage.new(self)
		storage.save()

	def to_dict(self):
		"""convert the object instance to dict format_
		"""
		diction = {}
		for key, value in self.__dict__.items():
			if key != '_sa_instance_state':
				if isinstance(value, datetime):
					diction[key] = value
				else:
					diction[key] = value
		return diction
	

	def delete(self):
		"""deletes an instance from storage"""
		from models import storage
		storage.delete(self)
		storage.save()
		
