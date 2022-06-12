from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, SelectField, SubmitField, StringField, ValidationError, validators

import re

from .models import Devices, Companies

from wtforms_sqlalchemy.orm import QuerySelectField


def validate_gps(form, field):
    data = []
    if field.data:
        for item in field.data.strip().split():
            try:
             data.append(float(item))
            except ValueError:
                raise ValidationError("GPS values must be converted to float")


class EditForm(FlaskForm):
    company = SelectField("Company", choices=[(0, None)], validators=[validators.Optional()])
    models = SelectField("Models", choices=[(0, None)], validate_choice=False)
    datetime = DateTimeLocalField("DateTime", validators=[validators.Optional()], format='%Y-%m-%dT%H:%M')
    gps_long = StringField("Longitude", validators=[validate_gps])
    gps_lat = StringField("Latitude", validators=[validate_gps])
    gps_long_ref = SelectField("Longitude ref", choices=[None, "N", "S"], validators=[validators.Optional()])
    gps_lat_ref = SelectField("Latitude ref", choices=[None, "E", "W"], validators=[validators.Optional()])
    submit = SubmitField("Change!")

