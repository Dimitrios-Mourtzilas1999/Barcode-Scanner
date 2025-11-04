from datetime import datetime
from sqlalchemy import CheckConstraint, Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(10),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'),nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):

    __tablename__ = "product"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,primary_key=True)
    barcode = db.Column(db.String(255),unique=True,nullable=False)
    data = db.Column(db.String(255), nullable=False)      # Encoded content
    filename = db.Column(db.String(255), nullable=False)  # Stored image filename
    desc = db.Column(db.String(100),server_default='')
    stock = db.Column(db.Integer,default=0)
    price = db.Column(db.Integer,default=.0)
    date_updated = db.Column(db.DateTime,default=datetime.now)
    date_created = db.Column(db.DateTime,default=datetime.now)

    def __repr__(self):
        return f"Generated QR Code {self.id} - {self.bar}"
    
class Roles(db.Model):
    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'user')",
            name='check_user_role'
        ),
        {'extend_existing': True}
    )
    id = db.Column(db.Integer,primary_key=True)
    role = db.Column(Enum('admin', 'user', name='user_roles'), nullable=False)
    user = db.relationship('User',backref='role',lazy=True)
