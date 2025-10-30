from flask import Blueprint,redirect,url_for
from forms import LoginForm
from models import User
from flask_login import login_user,logout_user,login_required


authbp = Blueprint('auth/',__name__)

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
