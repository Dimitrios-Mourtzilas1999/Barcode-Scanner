from flask import Blueprint

category = Blueprint('category',__name__,static_folder='static',static_url_path='/static',template_folder='templates')

@category.route('/register')
def registery_category():

    return "ddsd"