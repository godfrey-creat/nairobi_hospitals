#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.booking import Booking
from models.user import Users
from models.hospital import Hospitals
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Booking": Booking, "User": User, "Hospital": Hospital,
           }


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        NAIROBI_HOSPITALS_MYSQL_CLIENT = getenv('NAIROBI_HOSPTALS_MYSQL_CLIENT')
        NAIROBI_HOSPITALS_MYSQL_PWD = getenv('NAIROBI_HOSPITALS_MYSQL_PWD')
        NAIROBI_HOSPITALS_MYSQL_HOST = getenv('NAIROBI_HOSPITALS_MYSQL_HOST')
        NAIROBI_HOSPITALS_MYSQL_DB = getenv('NAIROBI_HOSPITALS_MYSQL_DB')
        NAIROBI_HOSPITALS_ENV = getenv('NAIROBI_HOSPITALS_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(NAIROBI_HOSPITALS_MYSQL_CLIENT,
                                             NAIROBI_HOSPITALS_MYSQL_PWD,
                                             NAIROBI_HOSPITALS_MYSQL_HOST,
                                             NAIROBI_HOSPITALS_MYSQL_DB))
        if NAIROBI_HOSPITALS_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def get(self, cls, id):
        """retrieves an object of a class with id"""
        obj = None
        if cls is not None and issubclass(cls, BaseModel):
            obj = self.__session.query(cls).filter(cls.id == id).first()
        return obj

    def count(self, cls=None):
        """retrieves the number of objects of a class or all (if cls==None)"""
        return len(self.all(cls))

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
