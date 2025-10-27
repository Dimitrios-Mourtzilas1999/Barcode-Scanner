from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from models import User
db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    login_manager.init_app(app)
    return app