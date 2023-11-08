from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=20), DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')