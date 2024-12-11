#!/usr/bin/python3
"""Database storage module"""
import os 
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


import models
import models.base_model
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class DBStorage:
	"""class blueprint to manage database storage for the project"""
	__engine = None
	__session = None
	__sessionMaker = None

	def __init__(self):
		"""Initilaize the database attributes"""
		user = os.getenv('HBNB_MYSQL_USER')
		passwd = os.getenv('HBNB_MYSQL_PWD')
		host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
		db_name = os.getenv('HBNB_MYSQL_DB')
		env = os.getenv('HBNB_ENV')

		# create the db engine 
		self.__engine = create_engine(f'mysql+mysqldb://{user}:{passwd}@{host}/{db_name}?unix_socket=/var/run/mysqld/mysqld.sock',
 		pool_pre_ping=True
		)

		# if enviroment is set to 'test' drop all tables
		if env == 'test':
			Base.metadata.drop_all(self.__engine)
	
	# Create methods for the CRUD(all, new, save, delete) operations
	
	def all(self, cls=None):
		"""Returns a dictionary of all the objects based on the class"""
		objects = {}
		if cls is None:
			for class_name, cls in models.classes.items():
				if issubclass(cls, models.base_model.Base):
					for obj in DBStorage.__session.query(cls):
						key = class_name + '.' + obj.id
						objects[key] = obj
		else:
			if not isinstance(cls, type):
				cls = models.classes[cls]
			for obj in DBStorage.__session.query(cls):
				key = cls.__name__ + '.' + obj.id
				objects[key] = obj
		return objects

						
 
	def new(self, obj):
		"""adds the object to current db session"""
		if obj is not None:
			try:
				self.__session.add(obj)
				self.__session.flush()
				self.__session.refresh(obj)
			except Exception as er:
				self.__session.rollback()
				raise er

	def save(self):
		"""commits all changes of the current db session"""
		return self.__session.commit()

	def delete(self, obj=None):
		"""deletes obj from current db session if obj not None"""
		if obj is not None:
			self.__session.delete(obj)
	
	def reload(self):
		"""Open a new MySQL session and create tables if necessary"""
		models.base_model.Base.metadata.create_all(self.__engine)
		if DBStorage.__sessionMaker is None:
			DBStorage.__sessionMaker = sqlalchemy.orm.scoped_session(
                sqlalchemy.orm.sessionmaker(bind=self.__engine)
            	)
		if self.__session is None:
			DBStorage.__session = self.__sessionMaker(expire_on_commit=False)

	def close(self):
		""" Closes teh session"""
		self.__session.remove()


