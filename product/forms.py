from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class ProductRegistrationForm(FlaskForm):

    barcode = IntegerField("Barcode", validators=[DataRequired()])
    desc = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    stock = IntegerField("Product Quantity", validators=[DataRequired()])
    image = FileField("Image", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Register Product")


class ProductEditForm(FlaskForm):

    barcode = IntegerField("Product ID", validators=[DataRequired()])
    desc = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    stock = IntegerField("Product Quantity", validators=[DataRequired()])

    submit = SubmitField("Edit product info")
