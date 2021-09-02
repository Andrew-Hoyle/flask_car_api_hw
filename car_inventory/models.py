from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash


# Import secrets file
import secrets


# Imporrts for Login Manager
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key = True)
    first_name = db.Column(db.String(150),nullable=True,default='')
    last_name = db.Column(db.String(150),nullable=True,default='')
    email = db.Column(db.String(150),nullable=False)
    password = db.Column(db.String, nullable=True,default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String,default='',unique=True)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    car = db.relationship('Drone', backref = 'User', lazy = True)

    def __init__( self, email, first_name='',last_name='',id='',password='',token='',g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
    
    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    

    class Vehicle(db.Model):
        id = db.Column(db.String, primary_key = True)
        make = db.Column(db.String(150))
        model = db.Column(db.String(50))
        price = db.Column(db.Numeric(precision=10,scale=2))
        msrp = db.Column(db.Numeric(precision=10,scale=2))
        engine_size = db.Column(db.Decimal(precision=1,scale=1))
        manufacturer = db.Column(db.String(50))
        user_token = db.Column(db.String, db.ForeignKey(User.token))

        