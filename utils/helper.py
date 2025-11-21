
from models import Category
from math import ceil


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_categories():
    empty_choice = ('', '----')  # placeholder option
    categories = [(c.id, c.cat_type) for c in Category.query.all()]
    return [empty_choice] + categories    


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