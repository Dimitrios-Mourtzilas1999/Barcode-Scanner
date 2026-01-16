from datetime import datetime
from sqlalchemy import CheckConstraint, Enum
from flask_login import UserMixin
from extensions import db
from hashlib import md5


class User(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.role if self.role else None,
        }

    def set_password(self, password):
        self.password = md5(password.encode("utf-8")).hexdigest()

    @property
    def is_admin(self):
        return self.role.role == "admin"


class Product(db.Model):

    __tablename__ = "product"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.String(255), unique=True, nullable=False)
    desc = db.Column(db.String(100), server_default="")
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0.0)
    image = db.Column(db.String(255), nullable=True)
    date_updated = db.Column(db.DateTime, default=datetime.now)
    date_created = db.Column(db.DateTime, default=datetime.now)
    cat_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)
    category = db.relationship("Category", backref="products", lazy=True)
    supplier = db.relationship("Supplier", backref="products", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "desc": self.desc,
            "stock": self.stock,
            "price": self.price,
            "category": self.category.cat_type if self.category else None,
            "date_updated": (
                self.date_updated.strftime("%Y-%m-%d") if self.date_updated else None
            ),
        }

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
    __tablename__ = "category"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cat_type = db.Column(db.String(100))


class Supplier(db.Model):
    __tablename__ = "suppliers"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
