from flask import Blueprint,redirect,url_for
from forms import LoginForm
from models import User
from flask_login import login_user,logout_user,login_required


authbp = Blueprint(
    'auth',                  # name of the blueprint
    __name__,
    static_folder='static',  # folder relative to this file
    static_url_path='/auth/static',  # URL to serve static files for this blueprint
    template_folder='templates'      # folder relative to this file
)


@authbp.route('/login',methods=["GET","POST"])
def login():

    lgForm = LoginForm()
    if lgForm.validate_on_submit():
        user = User.query.filter(lgForm.username.data).first()
        if user and user.check_password(lgForm.password.data):
            login_user()
            return redirect(url_for('dashboard'))


@authbp.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# auth/routes.py

from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required
from . import authbp
from models import User
from auth.forms import LoginForm


@authbp.route('/login',methods=["GET","POST"])
def login():

    lgForm = LoginForm()
    if lgForm.validate_on_submit():
        user = User.query.filter(lgForm.username.data).first()
        if user and user.check_password(lgForm.password.data):
            login_user()
            return redirect(url_for('dashboard'))


@authbp.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))