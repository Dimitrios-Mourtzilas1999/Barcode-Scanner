
from flask import Blueprint,url_for,redirect,render_template,flash
from .forms import LoginForm
from flask_login import login_user,login_required,logout_user
from models import User

authbp = Blueprint('auth',__name__,url_prefix='/auth')

@authbp.route('/login',methods=["GET","POST"])
def login():

    lgForm = LoginForm()
    if lgForm.validate_on_submit():
        user = User.query.filter(lgForm.username.data).first()
        if user and user.check_password(lgForm.password.data):
            login_user()
            return redirect(url_for('dashboard'))
        else:
            flash('Τα στοιχεία χρήστη είναι λάθος')
            return redirect('auth.login',form=lgForm)
    return render_template('auth/login.html',form=lgForm)


@authbp.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
