from flask import Blueprint,request
from forms import RegisterCategoryForm
from sqlalchemy.exc import DatabaseError
from models import Category,Product
from extensions import db

categorybp = Blueprint('category',__name__,static_folder='static',static_url_path='/static',template_folder='templates')

@categorybp.route('/register')
def register_category():

    rgCatForm = RegisterCategoryForm()
    if rgCatForm.validate_on_submit():
        category = Category(cat_type = rgCatForm.category_type.data)
        try:
            db.session.add(category)
            db.session.commit()
        except DatabaseError as dbe:
            db.session.rollback()
            print(f"[ERROR]: {dbe}")
        finally:
            db.session.close()
    return

@categorybp.route('/assign-product-to-category',methods=["POST"])
def assign_product_to_category():

    data = request.get_json()
    if not data:
        return {'status':'error','message':'Data could not be parsed'}
    
    barcode = data.get('barcode')
    products = db.session.query(Product).filter(Product.barcode.in_(barcode)).all()
    if products is None:
        return {'status':'error','message':'Product could not be found'}
    