from flask import redirect,url_for,flash,render_template,Blueprint
from .forms import LoginForm,PasswordResetForm
from models import User
from flask_login import login_user,logout_user,login_required
from extensions import db

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
        else:
            return redirect(url_for('auth.login'))

    return render_template('login.html',form=lgForm)


@authbp.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@authbp.route('/forgot-password', methods=["GET","POST"])
def forgot_password():
    resetForm = PasswordResetForm()
    if resetForm.validate_on_submit():
        user = User.query.filter_by(username=resetForm.username.data).first()
        if user:
            try:
                user.set_password(resetForm.password.data)  # properly set the new password
                db.session.commit()
                flash('Ο κωδικός σας ενημερώθηκε', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                db.session.rollback()
                print(f"[ERROR]: {e}")
                flash('Κάτι πήγε στραβά. Δοκιμάστε ξανά.', 'error')
        else:
            flash('Δεν υπάρχει χρήστης με αυτό το όνομα', 'error')
    return render_template('reset_password.html', form=resetForm)
