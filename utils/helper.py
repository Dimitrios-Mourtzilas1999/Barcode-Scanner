
from typing import OrderedDict
from models import Category, Supplier
from sqlalchemy import Integer, Float, String
from math import ceil
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_categories():
    empty_choice = (None, '----')
    items = [(c.id, c.cat_type) for c in Category.query.all()]
    items.sort(key=lambda x: x[1])   # sort by cat_type

    return OrderedDict([empty_choice] + items)

def paginate(query, page, per_page=20):
    """
    Paginate a SQLAlchemy query.
    
    Returns:
        items       -> items for the current page
        page        -> current page number
        pages       -> total number of pages
        total       -> total number of items
    """
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    pages = ceil(total / per_page)

    return items, page, pages, total



def get_suppliers():
    empty_choice = (None, '----')
    items = [(s.id, s.name) for s in Supplier.query.all()]
    items.sort(key=lambda x: x[1])   # sort by name
    return OrderedDict([empty_choice] + items)

