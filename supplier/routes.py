import datetime
from flask import (
    jsonify,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)
from sqlalchemy.exc import SQLAlchemyError
from .forms import SupplierRegistrationForm, SupplierEditForm
from extensions import db
from models import Category, Product, Supplier
from flask import Blueprint

supplierbp = Blueprint(
    "supplier",
    __name__,
    url_prefix="/supplier",
    static_folder="static",
    static_url_path="/static",
    template_folder="templates",
)


@supplierbp.route("/", methods=["GET", "POST"])
def suppliers():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    product_count = Supplier.query.join(Product).count()
    return render_template(
        "suppliers_index.html", suppliers=suppliers, product_count=product_count
    )


@supplierbp.route("/supplier/<int:supplier_id>/products")
def supplier_products(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    products = (
        Product.query.filter_by(supplier_id=supplier_id)
        .join(Category, isouter=True)
        .add_entity(Category)
        .all()
    )

    # Optional: simplify product list if you already have relationships
    products = supplier.products  # if Supplier → Product relationship exists

    return render_template(
        "supplier_products.html", supplier=supplier, products=products
    )


@supplierbp.route("/register", methods=["GET", "POST"])
def register_supplier():

    form = SupplierRegistrationForm()
    if form.validate_on_submit():
        supplier = (
            db.session.query(Supplier).filter(Supplier.name == form.name.data).first()
        )
        if supplier:
            flash("Ο προμηθευτής υπάρχει ήδη", "danger")
            return redirect(url_for("dashboard"))
        else:

            try:
                supplier = Supplier(
                    name=form.name.data, email=form.email.data, phone=form.phone.data
                )
                db.session.add(supplier)
                db.session.commit()
                return redirect(url_for("dashboard"))
            except Exception as e:
                print(e)
                db.session.rollback()
            finally:
                db.session.close()

    return render_template("register_supplier.html", form=form)


@supplierbp.route("/edit", methods=["GET", "POST"])
def edit_supplier():
    form = SupplierEditForm()

    # On GET, get barcode from query params to prefill the form
    if request.method == "GET":
        name = request.args.get("name", type=str)
        if name is None:
            flash("No name provided", "error")
            return redirect(url_for("dashboard"))

        supplier = Supplier.query.filter_by(name=name).first()
        if not supplier:
            flash("Supplier not found", "error")
            return redirect(url_for("dashboard"))

        # Prepopulate the form with product data
        form = SupplierEditForm(obj=supplier)

    # On POST, get barcode from the hidden field
    if form.validate_on_submit():
        name = form.name.data
        supplier = Supplier.query.filter_by(name=request.args.get("name", "")).first()
        if not supplier:
            flash("Supplier not found", "error")
            return redirect(url_for("dashboard"))

        # Update product from form
        form.populate_obj(supplier)
        try:
            db.session.commit()
            flash("Supplier updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Failed to update supplier: {str(e)}", "error")
        return redirect(url_for("dashboard"))

    return render_template("edit_supplier.html", form=form)


@supplierbp.route("/delete", methods=["POST"])
def delete():

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Could not read data"}), 400

    name = data.get("name", "")
    supplier = Supplier.query.filter(Supplier.name == name).first()

    try:
        db.session.delete(supplier)
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
