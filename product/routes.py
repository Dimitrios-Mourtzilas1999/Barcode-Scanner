from . import productbp
from flask import render_template, redirect, url_for, request, flash, current_app
from .forms import ProductRegistrationForm, ProductEditForm
from extensions import db
from models import Product
from werkzeug.utils import secure_filename
import os
from utils.helper import allowed_file


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
            return redirect(url_for("dashboard", message="Το προϊόν υπαρχει ήδη"))
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
