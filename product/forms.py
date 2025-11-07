from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ProductRegistrationForm(FlaskForm):

    product_id = IntegerField("Product ID", validators=[DataRequired()])
    product_name = StringField("Product Name", validators=[DataRequired()])
    product_price = IntegerField("Product Price", validators=[DataRequired()])
    product_quantity = IntegerField("Product Quantity", validators=[DataRequired()])

    submit = SubmitField("Register Product")


class ProductEditForm(FlaskForm):

    product_id = IntegerField("Product ID", validators=[DataRequired()])
    product_name = StringField("Product Name", validators=[DataRequired()])
    product_price = IntegerField("Product Price", validators=[DataRequired()])
    product_quantity = IntegerField("Product Quantity", validators=[DataRequired()])

    submit = SubmitField("Register Product")
