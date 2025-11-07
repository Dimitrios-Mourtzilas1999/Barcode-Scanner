from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class ProductRegistrationForm(FlaskForm):

    product_id = IntegerField("Product ID", validators=[DataRequired()])
    product_name = StringField("Product Name", validators=[DataRequired()])
    product_price = IntegerField("Product Price", validators=[DataRequired()])
    product_quantity = IntegerField("Product Quantity", validators=[DataRequired()])
    image = FileField("Image", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Register Product")


class ProductEditForm(FlaskForm):

    product_id = IntegerField("Product ID", validators=[DataRequired()])
    product_name = StringField("Product Name", validators=[DataRequired()])
    product_price = IntegerField("Product Price", validators=[DataRequired()])
    product_quantity = IntegerField("Product Quantity", validators=[DataRequired()])

    submit = SubmitField("Edit product info")
