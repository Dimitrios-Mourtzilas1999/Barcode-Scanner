
from extensions import create_app
from models import db

app = create_app()

with app.app_context():

    db.create_all()

@app.route('/',methods=["GET","POST"])
def index():
    lgForm = LoginForm()
    if lgForm.validate_on_submit():
        user = User.query.filter(lgForm.username.data).first()
        if user and user.check_password(lgForm.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Τα στοιχεία χρήστη δεν είναι σωστά','Success')
            return render_template('login.html',form=lgForm)
        

@app.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))






if __name__ == "__main__":

    app.run(host="localhost",port="8000")