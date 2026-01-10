from flask_wtf.form import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):

    username = StringField('Όνομα χρήστη',validators=[DataRequired()],render_kw={'class':'login-username'})
    password = PasswordField('Κωδικός',validators=[DataRequired()],render_kw={'class':'login-pwd'})
    submit = SubmitField('Σύνδεση',render_kw={'class':'btn'})

    



class PasswordResetForm(FlaskForm):
    username = StringField('Όνομα χρήστη',validators=[DataRequired()],render_kw={'class':'forgot-username'})
    password = PasswordField('Νέος κωδικός',validators=[DataRequired()],render_kw={'class':'forgot-pwd'})
    password_confirm = PasswordField('Επιβεβαίωση νέου κωδικού',validators=[DataRequired()],render_kw={'class':'forgot-pwd'})
    submit = SubmitField('Επαναφορά Κωδικού')
    