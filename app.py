from flask import render_template, redirect, url_for, request
from flask import Flask, jsonify
from flask_migrate import Migrate
from sqlalchemy import and_
from extensions import db, login_manager
from models import User, Product
from forms import AssignProductForm
import sys, os
import pymysql
from utils.helper import get_categories, get_suppliers, paginate


pymysql.install_as_MySQLdb()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


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
    from auth import authbp as auth_blueprint
    from product.routes import productbp as product_blueprint
    from category.routes import categorybp as category_blueprint
    from supplier.routes import supplierbp as supplier_blueprint

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


@app.route("/api/barcodes")
def barcodes():
    query = request.args.get("q", "")
    results = Product.query.filter(Product.barcode.like(f"%{query}%")).limit(10).all()
    barcodes_list = [p.barcode for p in results]
    return jsonify(barcodes_list)


@app.route("/filters", methods=["POST"])
def filters():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Could not read data"}), 400

    products = Product.query
    print(products.all())
    barcode = data.get("barcode")
    category = data.get("category")
    supplier = data.get("supplier")

    print(barcode, category, supplier)

    if barcode:
        products = products.filter(Product.barcode == barcode)

    if category:
        products = products.filter(Product.cat_id == category)

    if supplier:
        products = products.filter(Product.supplier_id == supplier)

    products, page, pages, total = paginate(products, 1, per_page=5)
    print(products)
    return jsonify(
        {
            "status": "success",
            "products": [p.to_dict() for p in products],
            "total": total,
            "pages": pages,
            "page": page,
        }
    )


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    page = request.args.get("page", 1, type=int)
    query = Product.query.order_by(Product.date_updated.desc())
    form = AssignProductForm()

    categories = get_categories()
    suppliers = get_suppliers()
    total = Product.query.count()
    products, page, pages, total = paginate(query, page, per_page=5)
    return render_template(
        "dashboard.html",
        products=products,
        page=page,
        pages=pages,
        total=total,
        categories=categories,
        suppliers=suppliers,
        form=form,
    )


@app.route("/fetch-product/<int:barcode>", methods=["POST"])
def fetch_product(barcode):
    product = Product.query.filter(Product.barcode == barcode).first()
    if not product:
        return jsonify({"status": "error", "message": "Product not found"})
    return jsonify({"status": "success", "info": product})


if __name__ == "__main__":

    app.run(host="localhost", port="8001")
