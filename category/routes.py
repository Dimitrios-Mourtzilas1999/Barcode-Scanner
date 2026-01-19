from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from sqlalchemy import func
from .forms import EditCategoryForm, RegisterCategoryForm
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from models import Category, Product, Supplier
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
    page = request.args.get("page", 1, type=int)

    categories = (
        db.session.query(
            Category.id,
            Category.cat_type,
            func.count(Product.id).label("product_count"),
        )
        .outerjoin(Product, Product.cat_id == Category.id)
        .group_by(Category.id)
        .order_by(Category.cat_type.asc())
        .all()
    )

    return render_template("categories_index.html", categories=categories, page=page)


@categorybp.route("/info", methods=["GET", "POST"])
def category_info():

    category = Category.query.filter_by(id=request.args.get("cat_id")).first()
    print(f"category: {category}")
    count = Product.query.filter_by(cat_id=category.id).count()
    if not category:
        flash("Η κατηγορία δεν βρέθηκε", "error")
        return redirect(url_for("category.categories"))

    return render_template("category_info.html", category=category, total=count)


@categorybp.route("/delete", methods=["GET", "POST"])
def delete_category():
    category = Category.query.filter_by(id=request.args.get("cat_id")).first()
    if not category:
        flash("Η κατηγορία δεν βρέθηκε", "error")
        return redirect(url_for("category.categories"))

    try:
        db.session.delete(category)
        db.session.commit()
        flash("Η κατηγορία διαγραφήκε", "success")
        return redirect(url_for("category.categories"))
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"[ERROR]: {e}")

    return render_template("delete_category.html", category=category)


@categorybp.route("/edit", methods=["GET", "POST"])
def edit_category():

    edit_category_form = EditCategoryForm()
    category = Category.query.filter_by(id=request.args.get("id")).first()
    if not category:
        flash("Η κατηγορία δεν βρέθηκε", "error")
        return redirect(url_for("category.categories"))

    if request.method == "POST":
        if edit_category_form.validate_on_submit():
            category.cat_type = edit_category_form.category_type.data
            db.session.commit()
            return redirect(url_for("category.categories"))
        else:
            print(edit_category_form.errors)

    return render_template(
        "edit_category.html", category=category, form=edit_category_form
    )


@categorybp.route("/register-category", methods=["GET", "POST"])
def register_category():
    rgCatForm = RegisterCategoryForm()
    if rgCatForm.validate_on_submit():
        category = Category(cat_type=rgCatForm.category_type.data)
        print(category)
        try:
            db.session.add(category)
            db.session.commit()
            return redirect(url_for("category.categories"))
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


@categorybp.route("/assign_product", methods=["POST"])
def assign_to_category():
    barcodes = [
        b.strip() for b in request.form.get("barcodes", "").split(",") if b.strip()
    ]
    category_id = request.form.get("categories")
    supplier_id = request.form.get("suppliers")
    print(barcodes, category_id, supplier_id)

    if not category_id:
        flash("Δεν επιλέξατε κατηγορία!", "warning")
        return redirect(url_for("dashboard"))

    if not supplier_id:
        flash("Δεν επιλέξατε προμηθευτή!", "warning")
        return redirect(url_for("dashboard"))

    category = Category.query.filter_by(id=int(category_id)).first()

    supplier = Supplier.query.filter_by(id=int(supplier_id)).first()
    if not category:
        flash("Η κατηγορία δεν βρέθηκε!", "error")
        return redirect(url_for("dashboard"))
    elif not supplier:
        flash("Ο προμηθευτής δεν βρέθηκε!", "error")
        return redirect(url_for("dashboard"))

    products = Product.query.filter(Product.barcode.in_(barcodes)).all()
    if not products:
        flash("Δεν βρέθηκαν προϊόντα για ενημέρωση.", "warning")
        return redirect(url_for("dashboard"))

    try:
        db.session.query(Product).filter(
            Product.id.in_([p.id for p in products])
        ).update(
            {"cat_id": category.id, "supplier_id": supplier.id},
            synchronize_session=False,
        )
        db.session.commit()

    except DatabaseError as e:
        db.session.rollback()
        print(f"[ERROR]: {e}")
        flash("Αποτυχία διαδικασίας καταχώρησης", "error")
        return redirect(url_for("dashboard"))

    flash(f"Επιτυχής καταχώρηση προϊόντων", "success")
    return redirect(url_for("dashboard"))
