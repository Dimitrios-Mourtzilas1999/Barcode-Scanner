from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class ProductRegistrationForm(FlaskForm):

    barcode = StringField("Barcode", validators=[DataRequired(), Length(max=255)])
    desc = StringField("Περιγραφή προϊόντος", validators=[DataRequired()])
    price = IntegerField("Τιμή προϊόντος", validators=[DataRequired()])
    stock = IntegerField("Ποσοτητα", validators=[DataRequired()])
    image = FileField("Αρχείο εικκόνας", validators=[FileAllowed(["jpg", "png"])])
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
