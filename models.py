from datetime import datetime
from sqlalchemy import CheckConstraint, Enum
from flask_login import UserMixin
from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)


class Product(db.Model):

    __tablename__ = "product"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.String(255), unique=True, nullable=False)
    desc = db.Column(db.String(100), server_default="")
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0.0)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    date_updated = db.Column(db.DateTime, default=datetime.now)
    date_created = db.Column(db.DateTime, default=datetime.now)
    cat_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=True)

    def __repr__(self):
        return f"Generated QR Code {self.id} - {self.barcode}"


class Roles(db.Model):
    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'user')", name="check_user_role"),
        {"extend_existing": True},
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(Enum("admin", "user", name="user_roles"), nullable=False)
    user = db.relationship(User, backref="role", lazy=True)


class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing':True}
    id = db.Column(db.Integer(),primary_key = True,autoincrement=True)
    cat_type = db.Column(db.String(100))
    product = db.relationship('Product', backref='category', lazy=True)
