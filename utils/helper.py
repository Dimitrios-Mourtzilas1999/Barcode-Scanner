
from models import Category

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_categories():
    empty_choice = ('', '----')  # placeholder option
    categories = [(c.id, c.cat_type) for c in Category.query.all()]
    return [empty_choice] + categories