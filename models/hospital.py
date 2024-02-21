#!/usr/bin/python3
""" holds class Garbage_collection_company"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Hospital(BaseModel, Base):
    """Representation of hospital"""
    if models.storage_t == "db":
        __tablename__ = 'hospitals'
        name = Column(String(128), nullable=False)
        service_types = relationship("Service_type", backref="hospital")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes garbage_collection_company"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def service_types(self):
            """getter for list of garbage_type instances related to the garbage_collection_company"""
            service_type_list = []
            all_service_types = models.storage.all(Service_type)
            for service_type in all_service_types.values():
                if service_type.hospital_id == self.id:
                    service_type_list.append(service_type)
            return service_type_list
