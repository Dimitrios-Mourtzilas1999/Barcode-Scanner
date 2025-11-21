from flask import jsonify, render_template, redirect, url_for, request, flash, current_app
from sqlalchemy.exc import SQLAlchemyError
from .forms import ProductRegistrationForm, ProductEditForm
from extensions import db
from models import Product
from werkzeug.utils import secure_filename
import os
from utils.helper import allowed_file
from flask import Blueprint

productbp = Blueprint(
    "product",
    __name__,
    url_prefix="/product",
    static_folder="static",
    static_url_path='/static',
    template_folder="templates",
)


@productbp.route("/register", methods=["GET", "POST"])
def register_product():

    form = ProductRegistrationForm()
    if form.validate_on_submit():
        product = (
            db.session.query(Product)
            .filter(Product.barcode == form.barcode.data)
            .first()
        )
        if product:
            flash('Το προϊόν υπάρχει ήδη','danger')
            return redirect(url_for("dashboard"))
        else:
            
            try:
                product = Product(barcode=form.barcode.data,desc=form.desc.data,stock=form.stock.data,price=form.price.data,image_file=form.image.data)
                db.session.add(product)
                db.session.commit()
                return redirect(url_for("dashboard"))
            except Exception as e:
                print(e)
                db.session.rollback()
            finally:
                db.session.close()

    return render_template("register_product.html", form=form)


@productbp.route("/edit", methods=["GET", "POST"])
def edit_product():
    form = ProductEditForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
    return render_template("edit_product.html", form=form)


@productbp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            flash("File uploaded successfully!")
            return redirect(url_for("uploaded_file", filename=filename))
    return render_template("upload.html")

@productbp.route('/delete',methods=["POST"])
def delete():

    data = request.get_json()
    if not data:
        return jsonify({'status':'error','message':'Could not read data'}),400
    
    barcodes = data.get('barcodes', [])
    products = Product.query.filter(Product.barcode.in_(barcodes)).all()

    try:
        for product in products:
            db.session.delete(product)
        db.session.commit()
        flash('Επιτυχης διαγραφη','success')
    except SQLAlchemyError as e:
        print(f"[ERROR]: {e}")
        flash('Πρόβλημα κατά την διαδικασία','danger')
        db.session.rollback()
        return jsonify({'status':'error','message':'Operation could not be completed'}),400
    return jsonify({'status':'success','message':'Successfull operation'}),200
