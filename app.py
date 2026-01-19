from flask import render_template, redirect, session, url_for, request
from flask import Flask, jsonify
from flask_migrate import Migrate
from extensions import db, login_manager
from models import Category, Supplier, User, Product
from forms import AssignProductForm
import sys, os
import pymysql
from utils.helper import paginate
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
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_suppliers = Supplier.query.count()
    total_stock_value = (
        db.session.query(db.func.sum(Product.price * Product.stock)).scalar() or 0
    )

    # === Category Pie Data ===
    category_counts = (
        db.session.query(Category.cat_type, db.func.count(Product.id))
        .outerjoin(Product, Product.cat_id == Category.id)
        .group_by(Category.cat_type)
        .all()
    )

    category_data = {
        "labels": [c[0] for c in category_counts],
        "values": [c[1] for c in category_counts],
    }

    # === Supplier Pie Data ===
    supplier_counts = (
        db.session.query(Supplier.name, db.func.count(Product.id))
        .outerjoin(Product, Product.supplier_id == Supplier.id)
        .group_by(Supplier.name)
        .all()
    )

    supplier_data = {
        "labels": [s[0] for s in supplier_counts],
        "values": [s[1] for s in supplier_counts],
    }

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_categories=total_categories,
        total_suppliers=total_suppliers,
        total_stock_value=total_stock_value,
        category_data=category_data,
        supplier_data=supplier_data,
    )


if __name__ == "__main__":

    app.run(host="localhost", port="8001")
