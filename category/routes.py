from flask import Blueprint,request,render_template,redirect,url_for
from .forms import RegisterCategoryForm,AssignProductForm
from sqlalchemy.exc import DatabaseError,SQLAlchemyError
from models import Category,Product
from extensions import db

categorybp = Blueprint('category',__name__,static_folder='static',static_url_path='/static',template_folder='templates')


@categorybp.route('/',methods=["GET"])
def categories():
    categories = Category.query.all()
    return render_template('categories_index.html',categories=categories)

@categorybp.route('/register', methods=["GET","POST"])
def register_category():
    rgCatForm = RegisterCategoryForm()
    if rgCatForm.validate_on_submit():
        category = Category(cat_type=rgCatForm.category_type.data)
        print(category)
        try:
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR]: {e}")
    else:
        print(rgCatForm.errors)
    return render_template('register_category.html', form=rgCatForm)

@categorybp.route('/assign-to-category',methods=["GET"])
def assign_to_category():
    apf = AssignProductForm()
    return render_template('assign.html',form=apf)

@categorybp.route('/set-to-category',methods=["POST"])
def assign_product_to_category():

    data = request.get_json()
    if not data:
        return {'status':'error','message':'Data could not be parsed'}
    
    barcode = data.get('barcode')
    products = db.session.query(Product).filter(Product.barcode.in_(barcode)).all()
    if products is None:
        return {'status':'error','message':'Product could not be found'}
    try:
        prs = db.session.query(Product).filter(Product.barcode.in_(data.get('barcode'))).all()
        for pr in prs:
            pr.cat_id = db.session.query(Category).filter(Category.cat_type == data.get('cat')).first().id
        db.session.commit()
    except DatabaseError as e:
        print(f"[ERROR]: {e}")
        db.session.rollback()
    finally:
        db.session.close()