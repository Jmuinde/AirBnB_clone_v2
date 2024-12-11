#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage 
depending on the selected mode of storage
"""
import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
    'Amenity': Amenity,
    'BaseModel': BaseModel,
    'City': City,
    'Place': Place,
    'Review': Review,
    'State': State,
    'User': User
}

storage = DBStorage() if os.getenv('HBNB_TYPE_STORAGE') == 'db' else FileStorage()
storage.reload()
