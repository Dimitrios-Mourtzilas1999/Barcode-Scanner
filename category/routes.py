from flask import Blueprint,request,render_template,redirect,url_for,flash
from .forms import RegisterCategoryForm,AssignProductForm
from sqlalchemy.exc import DatabaseError,SQLAlchemyError
from models import Category,Product
from extensions import db

categorybp = Blueprint('category',__name__,static_folder='static',static_url_path='/categories/static',template_folder='templates')


@categorybp.route('/list',methods=["GET"])
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



@categorybp.route('/assign-to-category', methods=["POST"])
def assign_to_category():

    data = request.get_json()
    barcodes = data.get('barcodes')
    category_id = data.get('category_id')

    category = Category.query.filter(Category.id == category_id).first()
    if not category:
        flash('Η κατηγορία δεν υπάρχει','error')
        return {'status': 400}

    products = Product.query.filter(Product.barcode.in_(barcodes)).all()
    print([p.id for p in products])
    try:
        for p in products:
            p.cat_id = category.id
        db.session.commit()
    except DatabaseError as e:
        print(f"[ERROR]: {e}")
        db.session.rollback()
        flash('Αποτυχία διαδικασία καταχώρησης','error')
        return {'status':500}
    
    flash(f'Επιτυχής καταχώρηση προϊόντων στην κατηγορία {category.cat_type}','success')
    return {'status':200}


