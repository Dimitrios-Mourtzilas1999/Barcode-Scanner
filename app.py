from flask import render_template
from extensions import create_app,db
app = create_app()
with app.app_context():

    db.create_all()

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():

    return render_template('dashboard.html')



if __name__ == "__main__":

    app.run(host="localhost",port="8000")