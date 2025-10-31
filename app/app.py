from flask import render_template,redirect,url_for
from . import create_app


app = create_app()

@app.route('/')
def index():

    return redirect(url_for('auth.login'))


@app.route('/dashboard',methods=["GET","POST"])
def dashboard():

    return render_template('dashboard.html')

if __name__ == "__main__":

    app.run(host="localhost",port="8000")