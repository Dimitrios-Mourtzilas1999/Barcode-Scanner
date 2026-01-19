from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

from models import Category, Supplier


class ProductRegistrationForm(FlaskForm):

    def get_categories():
        categories = Category.query.all()
        return [(category.id, category.cat_type) for category in categories]

    def get_suppliers():
        suppliers = Supplier.query.all()
        return [(supplier.id, supplier.name) for supplier in suppliers]

    barcode = StringField("Barcode", validators=[DataRequired(), Length(max=255)])
    desc = StringField("Περιγραφή προϊόντος", validators=[DataRequired()])
    price = IntegerField("Τιμή προϊόντος", validators=[DataRequired()])
    stock = IntegerField("Ποσοτητα", validators=[DataRequired()])
    image = FileField("Αρχείο εικκόνας", validators=[FileAllowed(["jpg", "png"])])
    categories = SelectField(
        "Κατηγορία", choices=get_categories, validators=[DataRequired()]
    )
    suppliers = SelectField(
        "Προμηθευτής", choices=get_suppliers, validators=[DataRequired()]
    )
    submit = SubmitField("Καταχώρηση προϊόντος")


class ProductEditForm(FlaskForm):

    barcode = StringField(
        "Κωδικός", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    desc = StringField(
        "Περιγραφή", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    price = IntegerField(
        "Τιμή",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    stock = IntegerField(
        "Ποσοτητα",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    image = FileField("Αρχείο εικκόνας", validators=[FileAllowed(["jpg", "png"])])

    submit = SubmitField("Υποβολή", render_kw={"class": "btn"})
