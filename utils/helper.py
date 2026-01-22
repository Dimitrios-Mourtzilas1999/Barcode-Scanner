from typing import OrderedDict
from models import Category, Supplier
from sqlalchemy import Integer, Float, String, distinct, func
from math import ceil

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# def get_categories():
#     return Category.query.order_by(Category.cat_type).all()

# def get_suppliers():
#     return Supplier.query.order_by(Supplier.name).all()


def paginate(query, model, page, per_page=20):
    total = query.with_entities(func.count(distinct(model.id))).scalar()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    pages = ceil(total / per_page)
    return items, page, pages, total


def get_categories():
    categories = Category.query.all()
    return [(category.id, category.cat_type) for category in categories]


def get_suppliers():
    suppliers = Supplier.query.all()
    return [(supplier.id, supplier.name) for supplier in suppliers]
