from flask import render_template,redirect,url_for
from flask import Flask
from models import User
from extensions import db,login_manager
from auth import authbp as auth_blueprint




def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'



    return app


app = create_app()
app.register_blueprint(auth_blueprint)

with app.app_context():

    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():

    return redirect(url_for('auth.login'))


@app.route('/dashboard',methods=["GET","POST"])
def dashboard():

    return render_template('dashboard.html')

if __name__ == "__main__":

    app.run(host="localhost",port="8000")