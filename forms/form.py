from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class HospitalRegistrationForm(FlaskForm):
    hospitalname = StringField('Hospital Name', validators=[DataRequired()])
    service_type_choices = [
        ('1', 'X-ray'),
        ('2', 'Orthopedic'),
        ('3', 'Dialysis'),
        ('4', 'Physiotherapy'),
        ('5', 'Dental'),
        ('6', 'Opticare'),
        ('7', 'Surgical'),
        ('8', 'Clinics')
    ]
    service_type = SelectField('Service Type', choices=service_type_choices, validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_no = StringField('Phone No', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    login_as_choices = [
        ('hospital', 'Hospital'),
        ('user', 'User')
    ]
    login_as = SelectField('Login As', choices=login_as_choices, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
