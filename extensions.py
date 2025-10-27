from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from auth import authbp as auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

