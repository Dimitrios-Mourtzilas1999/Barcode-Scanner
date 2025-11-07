from . import productbp
from flask import render_template, redirect, url_for
from .forms import ProductRegistrationForm, ProductEditForm
from extensions import db
from models import Product
from datetime import datetime


@productbp.route("/register", methods=["GET", "POST"])
def register_product():

    form = ProductRegistrationForm()
    if form.validate_on_submit():
        product = (
            db.session.query(Product)
            .filter(Product.barcode == form.product_id.data)
            .first()
        )
        if product:
            return redirect(url_for("dashboard", message="Το προϊόν υπαρχει ήδη"))
        try:
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
