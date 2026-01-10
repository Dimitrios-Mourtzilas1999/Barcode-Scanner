from flask import redirect,url_for,flash,render_template,Blueprint,request
from flask_login import current_user
from .forms import LoginForm,PasswordResetForm
from models import User
from flask_login import login_user,logout_user,login_required
from extensions import db
from hashlib import md5

authbp = Blueprint(
    'auth',                  # name of the blueprint
    __name__,
    static_folder='static',  # folder relative to this file
    static_url_path='/auth/static',  # URL to serve static files for this blueprint
    template_folder='templates'      # folder relative to this file
)


@authbp.route('/login', methods=['GET', 'POST'])
def login():
    lgForm = LoginForm()
    if request.method == 'POST':
         if lgForm.validate_on_submit():
            user = User.query.filter_by(username=lgForm.username.data,password=md5(lgForm.password.data.encode()).hexdigest()).first()
            if user:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Τα στοιχεία σύνδεσης είναι λάθος', 'error')

    return render_template('login.html', form=lgForm)



@authbp.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@authbp.route('/reset-password', methods=["GET","POST"])
def reset_password():
    resetForm = PasswordResetForm()
    if resetForm.validate_on_submit():
        newPassword = resetForm.password.data
        confirmPassword = resetForm.password_confirm.data
        if newPassword != confirmPassword:
            flash('Οι κωδικοι δεν ταιριαζουν', 'error')
            return redirect(url_for('auth.reset_password'), form=resetForm)
        
        user = User.query.filter_by(username=resetForm.username.data).first()
        if user:
            try:
                user.set_password(resetForm.password.data)  # properly set the new password
                db.session.commit()
                flash('Ο κωδικός σας ενημερώθηκε', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                print(f"[ERROR]: {e}")
                flash('Κάτι πήγε στραβά. Δοκιμάστε ξανά.', 'error')
        else:
            flash('Δεν υπάρχει χρήστης με αυτό το όνομα', 'error')
    return render_template('reset_password.html', form=resetForm)
