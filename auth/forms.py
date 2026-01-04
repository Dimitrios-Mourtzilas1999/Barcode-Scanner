from flask_wtf.form import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):

    username = StringField('Username',validators=[DataRequired()],render_kw={'class':'login-username'})
    password = PasswordField('Password',validators=[DataRequired()],render_kw={'class':'login-pwd'})
    submit = SubmitField('Login',render_kw={'class':'btn'})

    



class PasswordResetForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()],render_kw={'class':'forgot-pwd'})
    password_confirm = PasswordField('Confirm password',validators=[DataRequired()],render_kw={'forgot-pwd'})
    submit = SubmitField('Reset password')
    