from flask import render_template, redirect, url_for, request
from flask import Flask, jsonify
from flask_migrate import Migrate
from sqlalchemy import and_
from extensions import db, login_manager
from models import Category, Supplier, User, Product
from category.forms import AssignProductForm
import sys, os
import pymysql
from utils.helper import get_categories,get_suppliers, paginate


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


@app.route('/apply_filters', methods=['POST'])
def apply_filters():

    data = request.form
    print(data)
    return jsonify({'status':'success'})

@app.route('/products', methods=['POST'])
def products():
    req = request.get_json()

    # Draw, start, length from DataTables
    draw = req.get('draw', 1)
    start = req.get('start', 0)
    length = req.get('length', 10)

    filters = req.get('filters', {})

    # Base query
    query = db.session.query(Product).outerjoin(Product.category).outerjoin(Product.supplier)

    # ----------------------------
    # Apply filters
    # ----------------------------
    conditions = []
    if filters.get('barcode'):
        conditions.append(Product.barcode.ilike(f"%{filters['barcode']}%"))
    if filters.get('category'):
        conditions.append(Category.cat_type.ilike(f"%{filters['category']}%"))
    if filters.get('supplier'):
        conditions.append(Supplier.name.ilike(f"%{filters['supplier']}%"))

    if conditions:
        query = query.filter(and_(*conditions))

    # Total rows before filtering
    recordsTotal = db.session.query(Product).count()
    # Total rows after filtering
    recordsFiltered = query.count()

    # ----------------------------
    # Ordering
    # ----------------------------
    order = req.get('order', [])
    # Map DataTables columns to SQLAlchemy columns
    column_map = {
        1: Product.barcode,
        2: Product.desc,
        3: Product.stock,
        4: Product.price,
        5: Product.date_updated,
        6: Category.cat_type,
        7: Supplier.name
    }
    if order:
        col_idx = order[0]['column']
        direction = order[0]['dir']
        col_attr = column_map.get(col_idx)
        if col_attr is not None:
            query = query.order_by(col_attr.asc() if direction == 'asc' else col_attr.desc())

    # ----------------------------
    # Pagination
    # ----------------------------
    rows = query.offset(start).limit(length).all()

    # ----------------------------
    # Build response
    # ----------------------------
    data = []
    for p in rows:
        data.append({
            "barcode": p.barcode,
            "desc": p.desc,
            "stock": p.stock,
            "price": float(p.price) if p.price else 0,
            "updated": p.date_updated.strftime("%Y-%m-%d") if p.date_updated else "-",
            "category": p.category.cat_type if p.category else "-",
            "supplier": p.supplier.name if p.supplier else "-"
        })

    return jsonify({
        "draw": draw,
        "recordsTotal": recordsTotal,
        "recordsFiltered": recordsFiltered,
        "data": data
    })


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    page = request.args.get("page", 1, type=int)
    query = Product.query.order_by(Product.date_updated.desc())

    print(request.args)
    # Map relationship query params to related model attributes
    # relationship_fields = {
    #     "category": "cat_type",  # query param 'category' filters Category.cat_type
    # }

    # for key, value in request.args.items():
    #     if not value or key == "page":
    #         continue

    #     if hasattr(Product, key):
    #         column = getattr(Product, key)

    #         # Detect relationship
    #         if hasattr(column.property, "direction"):  # relationship
    #             rel_attr_name = relationship_fields.get(key)
    #             if rel_attr_name:
    #                 query = query.filter(column.has(**{rel_attr_name: value}))
    #         else:
    #             query = query.filter(column == value)

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
        return jsonify({'status': 'error','message':'Could not read data'}), 400

    query = Product.query

    joined = set()

    for key, value in data.items():
        if value is None or value == "":
            continue

        print(key, value)

        if key == "category":
            if "category" not in joined:
                query = query.outerjoin(Category, Product.cat_id == Category.id)
                joined.add("category")
            query = query.filter(Category.cat_type.ilike(f"%{value}%"))

        elif key == "supplier":
            if "supplier" not in joined:
                query = query.outerjoin(Supplier, Product.supplier_id == Supplier.id)
                joined.add("supplier")
            query = query.filter(Supplier.name.ilike(f"%{value}%"))

        elif hasattr(Product, key):
            col = getattr(Product, key)
            query = query.filter(col == value)

    results = query.all()
    print(results)
    products = [p.to_dict() for p in results]

    return jsonify({'status':'success','results':products})
 
@app.route("/fetch-product/<int:barcode>", methods=["POST"])
def fetch_product(barcode):
    product = Product.query.filter(Product.barcode == barcode).first()
    if not product:
        return jsonify({"status": "error", "message": "Product not found"})
    return jsonify({"status": "success", "info": product})

if __name__ == "__main__":

    app.run(host="localhost", port="8001")
