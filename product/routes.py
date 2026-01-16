import datetime
from flask import (
    jsonify,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
)
from sqlalchemy.exc import SQLAlchemyError
from .forms import ProductRegistrationForm, ProductEditForm
from extensions import db
from models import Product
from werkzeug.utils import secure_filename
import os
from utils.helper import allowed_file
from flask import Blueprint
from werkzeug.utils import secure_filename
import os, qrcode

productbp = Blueprint(
    "product",
    __name__,
    url_prefix="/product",
    static_folder="static",
    static_url_path="/static",
    template_folder="templates",
)


@productbp.route("/register", methods=["GET", "POST"])
def register_product():
    form = ProductRegistrationForm()

    if form.validate_on_submit():
        product = Product.query.filter_by(barcode=form.barcode.data).first()
        if product:
            flash("Το προϊόν υπάρχει ήδη", "danger")
            return redirect(url_for("dashboard"))

        image_filename = None
        if form.image.data:
            image = form.image.data
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_filename = f"{form.barcode.data}_{filename}"
                image.save(
                    os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
                )
            else:
                flash("Μη έγκυρος τύπος αρχείου εικόνας", "danger")
                return redirect(url_for("dashboard"))

        try:
            product = Product(
                barcode=form.barcode.data,
                desc=form.desc.data,
                stock=form.stock.data,
                price=form.price.data,
                date_created=datetime.datetime.now(),
                image=image_filename if image_filename else None,
            )
            db.session.add(product)
            db.session.commit()
            flash("Το προϊόν καταχωρήθηκε επιτυχώς!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Σφάλμα κατά την καταχώρηση: {e}", "danger")
        finally:
            db.session.close()

    return render_template("register_product.html", form=form)


@productbp.route("/edit", methods=["GET", "POST"])
def edit_product():
    form = ProductEditForm()
    product = None

    # --- GET ---
    if request.method == "GET":
        barcode = request.args.get("barcode", type=str)
        if not barcode:
            flash("No barcode provided", "error")
            return redirect(url_for("dashboard"))

        product = Product.query.filter_by(barcode=barcode).first()
        if not product:
            flash("Product not found", "error")
            return redirect(url_for("dashboard"))

        form = ProductEditForm(obj=product)

        # Generate QR code
        qr_filename = f"{product.barcode}.png"
        qr_path = os.path.join(current_app.static_folder, "qrcodes", qr_filename)
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(product.barcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)

        return render_template(
            "edit_product.html", form=form, product=product, qr_filename=qr_filename
        )

    # --- POST ---
    if form.validate_on_submit():
        product = Product.query.filter_by(barcode=form.barcode.data).first()
        if not product:
            flash("Product not found", "error")
            return redirect(url_for("dashboard"))

        # Handle image upload
        if form.image.data and form.image.data.filename != "":
            image = form.image.data
            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_filename = f"{form.barcode.data}_{filename}"

                if product.image:
                    old_path = os.path.join(
                        current_app.config["UPLOAD_FOLDER"], product.image
                    )
                    if os.path.exists(old_path):
                        os.remove(old_path)

                image.save(
                    os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
                )
                product.image = image_filename
            else:
                flash("Μη έγκυρος τύπος αρχείου εικόνας", "danger")
                return redirect(
                    url_for("product.edit_product", barcode=product.barcode)
                )

        # Update other fields
        product.desc = form.desc.data
        product.stock = form.stock.data
        product.price = form.price.data
        product.date_updated = datetime.datetime.now()

        try:
            db.session.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Failed to update product: {str(e)}", "error")
            return redirect(url_for("product.edit_product", barcode=product.barcode))


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


@productbp.route("/delete", methods=["POST"])
def delete():

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Could not read data"}), 400

    barcodes = data.get("barcodes", [])
    products = Product.query.filter(Product.barcode.in_(barcodes)).all()

    try:
        for product in products:
            db.session.delete(product)
        db.session.commit()
        flash("Επιτυχης διαγραφη", "success")
    except SQLAlchemyError as e:
        print(f"[ERROR]: {e}")
        flash("Πρόβλημα κατά την διαδικασία", "danger")
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": "Operation could not be completed"}),
            400,
        )
    return jsonify({"status": "success", "message": "Successfull operation"}), 200
