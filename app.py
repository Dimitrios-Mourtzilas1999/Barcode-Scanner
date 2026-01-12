from flask import render_template, redirect, session, url_for, request
from flask import Flask, jsonify
from flask_migrate import Migrate
from extensions import db, login_manager
from models import Category, Supplier, User, Product
from forms import AssignProductForm
import sys, os
import pymysql
from utils.helper import get_categories, get_suppliers, paginate
from config import Config
from auth.routes import authbp as auth_blueprint
from product.routes import productbp as product_blueprint
from category.routes import categorybp as category_blueprint
from supplier.routes import supplierbp as supplier_blueprint

pymysql.install_as_MySQLdb()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static",
    )
    app.config.from_object(Config)  # config.py at project root

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(supplier_blueprint)

    Migrate(app, db)

    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():

    return redirect(url_for("auth.login"))


@app.route("/filters", methods=["POST"])
def filters():
    data = request.get_json() or {}
    print(data)

    session["filters"] = {
        "barcode": data.get("barcode") or None,
        "category": data.get("category") or None,
        "supplier": data.get("supplier") or None,
        "sort": data.get("sort") or "date_updated",
        "order": data.get("order") or "desc",
    }

    return jsonify({"status": "success", "filters": session["filters"]})


@app.route("/clear-filters", methods=["POST"])
def clear_filters():
    session.pop("filters", None)
    return jsonify({"status": "success"})


@app.route("/dashboard", methods=["GET"])
def dashboard():
    page = request.args.get("page", 1, type=int)

    filters = session.get("filters", {})

    sort = request.args.get("sort", "date_updated")
    order = request.args.get("order", "desc")

    query = Product.query

    if filters.get("barcode"):
        query = query.filter(Product.barcode == filters["barcode"])

    if filters.get("category"):
        query = query.filter(Product.cat_id == filters["category"])

    if filters.get("supplier"):
        query = query.filter(Product.supplier_id == filters["supplier"])

    if sort in ["category", "supplier"]:
        if sort == "category":
            query = query.join(Category, Product.cat_id == Category.id)
        elif sort == "supplier":
            query = query.join(Supplier, Product.supplier_id == Supplier.id)

    sort_map = {
        "barcode": Product.barcode,
        "desc": Product.desc,
        "stock": Product.stock,
        "price": Product.price,
        "updated_at": Product.date_updated,
        "category": Category.cat_type,
        "supplier": Supplier.name,
    }

    sort_col = sort_map.get(sort, Product.date_updated)
    query = query.order_by(sort_col.asc() if order == "asc" else sort_col.desc())
    products, page, pages, total = paginate(query, page, per_page=3)

    return render_template(
        "dashboard.html",
        products=products,
        page=page,
        pages=pages,
        total=total,
        categories=get_categories(),
        suppliers=get_suppliers(),
        active_filters=filters,  # useful for UI
        form=AssignProductForm(),
    )


if __name__ == "__main__":

    app.run(host="localhost", port="8001")
