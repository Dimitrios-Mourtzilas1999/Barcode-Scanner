
from flask import Blueprint,url_for,redirect,render_template,flash
from .forms import LoginForm
from flask_login import login_user,login_required,logout_user
from main.models import User
from hashlib import sha256

authbp = Blueprint('auth',__name__,url_prefix='/auth')

@authbp.route('/login',methods=["GET","POST"])
def login():

    lgForm = LoginForm()
    if lgForm.validate_on_submit():
        username = lgForm.username.data
        password= lgForm.password.data
        hashed = sha256(password.encode()).hexdigest()
        print(hashed)
        user = User.query.filter(User.username == username).first()
        if user and user.password == hashed:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Τα στοιχεία χρήστη είναι λάθος','error')
            return render_template('auth/login.html',form=lgForm)


    return render_template('auth/login.html',form=lgForm)


@authbp.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
