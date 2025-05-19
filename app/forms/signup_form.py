from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User


def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')

def phone_number_exists(form, field):
    # Checking if phone number exists
    phone_number = field.data
    user = User.query.filter(User.phone_number == phone_number).first()
    if user:
        raise ValidationError('Phone number is already in use.')

class SignUpForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    phone_number = StringField('phone_number', validators=[DataRequired(), phone_number_exists])
    email = StringField('email', validators=[DataRequired(), user_exists])
    profile_image = StringField('profile_image')
    password = StringField('password', validators=[DataRequired()])
