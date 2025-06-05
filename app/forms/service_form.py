from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, MultipleFileField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, NumberRange


class ServiceForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('description', validators=[DataRequired(), Length(max=1000)])
    price = IntegerField('price', validators=[DataRequired(), NumberRange(min=0)])
    details = TextAreaField('details', validators=[DataRequired(), Length(max=2000)])
    images = MultipleFileField('Image File', validators=[
    FileAllowed(['jpg', 'jpeg', 'png', 'gif'])
    ])
