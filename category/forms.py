from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,SubmitField,SelectField
from collections import OrderedDict
from utils.helper import get_categories

class RegisterCategoryForm(FlaskForm):

    category_type = StringField('Κατηγορία',validators=[DataRequired()])
    submit = SubmitField('Καταχώρηση')
    

class AssignProductForm(FlaskForm):
    
    empty_key = ''
    empty_value = '-----'
    categories = OrderedDict([(empty_key, empty_value)] + get_categories())
    cat_dropdown = SelectField(choices=categories)
    submit =  SubmitField('Ολοκλήρωση')
    