from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from .forms import RegisterCategoryForm, AssignProductForm
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from models import Category, Product
from extensions import db

categorybp = Blueprint(
    "category",
    __name__,
    static_folder="static",
    static_url_path="/categories/static",
    template_folder="templates",
    url_prefix="/category",
)


@categorybp.route("/list", methods=["GET"])
def categories():
    categories = Category.query.all()
    return render_template("categories_index.html", categories=categories)


@categorybp.route("/register-category", methods=["GET", "POST"])
def register_category():
    rgCatForm = RegisterCategoryForm()
    if rgCatForm.validate_on_submit():
        category = Category(cat_type=rgCatForm.category_type.data)
        print(category)
        try:
            db.session.add(category)
            db.session.commit()
            return redirect(url_for("dashboard"))
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR]: {e}")
    else:
        print(rgCatForm.errors)
    return render_template("register_category.html", form=rgCatForm)


@categorybp.route("/get-categories", methods=["POST"])
def get_categories():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Could not read data"}), 400
    id = data.get("category_id")
    category = Category.query.filter(Category.id == id).first()
    return jsonify({"status": "success", "category": category})


@categorybp.route("/assign_to_category", methods=["POST"])
def assign_to_category():
    barcodes = [
        b.strip() for b in request.form.get("barcodes", "").split(",") if b.strip()
    ]
    category_id = request.form.get("categories")
    print(barcodes, category_id)
    if not barcodes:
        flash("Δεν επιλέξατε προϊόντα!", "warning")
        return redirect(url_for("dashboard"))

    if not category_id:
        flash("Δεν επιλέξατε κατηγορία!", "warning")
        return redirect(url_for("dashboard"))

    category = Category.query.filter_by(id=int(category_id)).first()
    if not category:
        flash("Η κατηγορία δεν βρέθηκε!", "error")
        return redirect(url_for("dashboard"))

    products = Product.query.filter(Product.barcode.in_(barcodes)).all()
    if not products:
        flash("Δεν βρέθηκαν προϊόντα για ενημέρωση.", "warning")
        return redirect(url_for("dashboard"))

    try:
        db.session.query(Product).filter(
            Product.id.in_([p.id for p in products])
        ).update({"cat_id": category.id}, synchronize_session=False)
        db.session.commit()

    except DatabaseError as e:
        db.session.rollback()
        print(f"[ERROR]: {e}")
        flash("Αποτυχία διαδικασίας καταχώρησης", "error")
        return redirect(url_for("dashboard"))

    flash(
        f"Επιτυχής καταχώρηση προϊόντων στην κατηγορία {category.cat_type}", "success"
    )
    return redirect(url_for("dashboard"))
