from flask import Flask
from flask_migrate import Migrate
from .extensions import db, login_manager
from auth import authbp as auth_blueprint
import pymysql

pymysql.install_as_MySQLdb()
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # config.py at project root

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(auth_blueprint)

    Migrate(app, db)

    return app