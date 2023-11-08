from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

from app.models import User

# What I am doing below is just creating two functions that will be used for validations...
# Like Length(), DataRequired(), etc...
# The difference is that Length() and anothers are already built in...
# But if they weren't we would need to do the same thing as below

# Checks if the username is already registered in the db
def validate_username(form, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError('This username was already choosen. Please type another one.')

# Checks if the email is already registered in the db    
def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('This email is already in use. Please type another one.')   

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=20), DataRequired(), validate_username])
    email = EmailField('Email', validators=[DataRequired(), validate_email])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')