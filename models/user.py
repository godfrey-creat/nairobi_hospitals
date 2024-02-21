#!/usr/bin/python3
""" Holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """Representation of a client """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        phone = Column(Integer, nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        garbage_type = relationship(
            "service_type",
            cascade="all, delete, delete-orphan",
            backref="user"
        )
        hospital = relationship(
            "hospital",
            cascade="all, delete, delete-orphan",
            backref="user"
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        phone = ""
        latitude = None
        longitude = None

    def __init__(self, *args, **kwargs):
        """Initializes client"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name: str, value) -> None:
        """Sets an attribute of this class to a given value."""
        if name == 'password' and isinstance(value, str):
            m = hashlib.md5(bytes(value, 'utf-8'))
            super().__setattr__(name, m.hexdigest())
        else:
            super().__setattr__(name, value)

    def update_location(self, latitude, longitude):
        """Update client's geolocation"""
        self.latitude = latitude
        self.longitude = longitude
        models.storage.save()

    def get_location(self):
        """Retrieve client's geolocation"""
        return self.latitude, self.longitude
