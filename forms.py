# -*- coding: utf-8 -*-
# itf-taekwon-do/forms.py
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email

    #email = StringField('Email', validators=[DataRequired(), Email()])
    #password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(Form):
    team = StringField('Jméno týmu', validators=[DataRequired()])
    first_name = StringField('Jméno', validators=[DataRequired()])
    last_name = StringField('Přímení', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Heslo', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Heslo znovu')
