from flask import render_template, redirect, url_for
from flask import Flask
from flask_migrate import Migrate
from extensions import db, login_manager
from models import User, Product
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
    from product import productbp as product_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(product_blueprint)

    Migrate(app, db)

    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():

    return redirect(url_for("auth.login"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    products = db.session.query(Product).all()
    return render_template("dashboard.html", products=products)


if __name__ == "__main__":

    app.run(host="localhost", port="8001")
