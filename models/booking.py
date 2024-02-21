#!/usr/bin/python3
"""Holds class Booking"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

class Booking(BaseModel, Base):
    """Representation of a booking"""
    if models.storage_t == 'db':
        __table__ = 'bookings'
        booking_id = Column(String(60), Foreignkey('bookings.id'), nullable=False)
        client_id = Column(String(60), Foreignkey('clients.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        booking_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Bookings"""
        super().__init__(*args, **kwargs)
