from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed



class ProductRegistrationForm(FlaskForm):

    barcode = StringField("Barcode", validators=[DataRequired(), Length(max=255)])
    desc = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    stock = IntegerField("Product Quantity", validators=[DataRequired()])
    image = FileField("Image", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Register Product")


class ProductEditForm(FlaskForm):

    barcode = IntegerField(
        "Product ID", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    desc = StringField(
        "Product Name", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    price = IntegerField(
        "Product Price",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    stock = IntegerField(
        "Product Quantity",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    submit = SubmitField("Edit product info", render_kw={"class": "btn"})