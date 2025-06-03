from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class AppointmentForm(FlaskForm):
    appointment_date = StringField('appointment_date', validators=[DataRequired()])

    def validate_appointment_date(form, field):
        try:
            datetime.strptime(field.data, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValidationError("Date must be in format YYYY-MM-DD HH:MM")
