from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, SubmitField,EmailField
from wtforms.validators import DataRequired



class SupplierRegistrationForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    email = EmailField('Email',validators=[DataRequired()])
    phone = IntegerField('Phone',validators=[DataRequired()])
    submit = SubmitField('Submit',render_kw={'class':'btn btn-primary'})

class SupplierEditForm(FlaskForm):


    name = StringField(
        "Supplier Name", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    phone = IntegerField(
        "Supplier Phone",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    email = EmailField(
        "Supplier Email",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    submit = SubmitField("Edit supplier info", render_kw={"class": "btn btn-primary"})