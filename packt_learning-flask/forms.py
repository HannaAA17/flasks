from flask_wtf import Form

from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length


class SignupForm(Form):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign Up')


class loginForm(Form):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log in')


class AddressForm(Form):
    address = StringField('Address', validators=[DataRequired('Please enter an address.')])
    submit = SubmitField('Search')

