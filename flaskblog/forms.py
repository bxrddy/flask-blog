from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flaskblog.models import User


# Registration Form
class RegistrationForm(FlaskForm):

	username 		  =  StringField('Username', validators = [DataRequired(), Length(min = 2, max = 20)])
	email 			  =  StringField('Email', validators = [DataRequired(), Email()])
	password 		  =  PasswordField('Password', validators = [DataRequired()])
	confirm_password  =  PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit 			  =  SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('This username is already taken. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('This email is already taken. Please choose a different one.')

# Login Form
class LoginForm(FlaskForm):

	email 			  =  StringField('Email', validators = [DataRequired(), Email()])
	password 		  =  PasswordField('Password', validators = [DataRequired()])
	remember		  =  BooleanField('Remember Me')
	submit 			  =  SubmitField('Login')