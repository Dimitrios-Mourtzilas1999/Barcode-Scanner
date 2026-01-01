from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField
from models import Supplier,Category

class AssignProductForm(FlaskForm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories.choices = [
            (str(c.id), c.cat_type) for c in Category.query.all()
        ]
        self.suppliers.choices = [(s.id,s.name) for s in Supplier.query.all()]

    categories = SelectField(
        "Επιλογή Κατηγορίας", choices=[], render_kw={"class": "categories"}
    )
    suppliers = SelectField('Επιλογή Προμηθευτή',choices = [],render_kw={'class':'suppliers'})
    
    submit = SubmitField("Ολοκλήρωση", render_kw={"class": "btn btn-primary assign-submit"})
