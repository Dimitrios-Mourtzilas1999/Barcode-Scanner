from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,SubmitField,SelectField

from utils.helper import get_categories

class RegisterCategoryForm(FlaskForm):

    category_type = StringField('Κατηγορία',validators=[DataRequired()])
    submit = SubmitField('Καταχώρηση')
    

class AssignProductForm(FlaskForm):
    
    cat_type = SelectField('Επιλογή Κατηγορίας',choices=get_categories())
    submit =  SubmitField('Ολοκλήρωση')
    