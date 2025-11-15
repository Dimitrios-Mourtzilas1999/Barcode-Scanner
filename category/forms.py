from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,SubmitField,SelectField
from models import Category
from extensions import db

class RegisterCategoryForm(FlaskForm):

    category_type = StringField('Κατηγορία',validators=[DataRequired()])
    submit = SubmitField('Καταχώρηση')
    

class AssignProductForm(FlaskForm):
    

    def __init__(self,  **kwargs):
        super().__init__( **kwargs)
        self.categories.choices = [(str(c.id), c.cat_type) for c in Category.query.all()]

    categories = SelectField('Επιλογή Κατηγορίας', choices=[],render_kw={'class':'categories'})
    submit =  SubmitField('Ολοκλήρωση',render_kw={'class':'submit'})
    