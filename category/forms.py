from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,SubmitField


class RegisterCategoryForm(FlaskForm):

    category_type = StringField('Κατηγορία',validators=[DataRequired()])
    submit = SubmitField('Καταχώρηση')

