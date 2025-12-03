from flask import render_template, redirect, url_for, request
from flask import Flask, jsonify
from flask_migrate import Migrate
from extensions import db, login_manager
from models import User, Product
from sqlalchemy.orm import class_mapper
from category.forms import AssignProductForm
from utils.helper import get_categories, get_suppliers, paginate
import sys, os
import pymysql


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

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(category_blueprint)

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


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    page = request.args.get("page", 1, type=int)
    query = Product.query.order_by(Product.date_updated.desc())

    print(request.args)
    # Map relationship query params to related model attributes
    relationship_fields = {
        "category": "cat_type",  # query param 'category' filters Category.cat_type
    }

    for key, value in request.args.items():
        if not value or key == "page":
            continue

        if hasattr(Product, key):
            column = getattr(Product, key)

            # Detect relationship
            if hasattr(column.property, "direction"):  # relationship
                rel_attr_name = relationship_fields.get(key)
                if rel_attr_name:
                    query = query.filter(column.has(**{rel_attr_name: value}))
            else:
                query = query.filter(column == value)

    # Pagination
    products, page, pages, total = paginate(query, page, per_page=5)

    # Additional context
    categories = get_categories()
    suppliers = get_suppliers()
    form = AssignProductForm()

    return render_template(
        "dashboard.html",
        form=form,
        products=products,
        page=page,
        pages=pages,
        total=total,
        categories=categories,
        suppliers=suppliers,
    )


@app.route('/filters', methods=['POST'])
def filters():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Could not read data'}), 400

    query = Product.query


    results = query.all()
    products = [p.to_dict() for p in results]

    return jsonify({'status': 'success', 'results': products})


@app.route("/fetch-product/<int:barcode>", methods=["POST"])
def fetch_product(barcode):
    product = Product.query.filter(Product.barcode == barcode).first()
    if not product:
        return jsonify({"status": "error", "message": "Product not found"})
    return jsonify({"status": "success", "info": product})

if __name__ == "__main__":

    app.run(host="localhost", port="8001")
