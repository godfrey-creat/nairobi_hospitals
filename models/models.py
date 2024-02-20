from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False,default='client')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"Users('{self.first_name}', '{self.last_name}', '{self.email}')"

class Hospital(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    hospitalname = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False,default='hospital')
    service_type = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"Hospital('{self.hospitalname}', '{self.email}', '{self.phone_no}')"
