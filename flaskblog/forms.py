from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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
			raise ValidationError('This email is already registered. Please choose a different one.')


# Login Form
class LoginForm(FlaskForm):

	email  		=  StringField('Email', validators = [DataRequired(), Email()])
	password 	=  PasswordField('Password', validators = [DataRequired()])
	remember	=  BooleanField('Remember Me')
	submit 		=  SubmitField('Login')


# Update User Account Form
class UpdateAccountForm(FlaskForm):

	username 	=  StringField('Username', validators = [DataRequired(), Length(min = 2, max = 20)])
	email 		=  StringField('Email', validators = [DataRequired(), Email()])
	picture 	=  FileField('Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
	submit 		=  SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('This username is already taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('This email is already taken. Please choose a different one.')


# Create Post Form
class PostForm(FlaskForm):

	title = StringField('Title', validators = [DataRequired()])
	content = TextAreaField('Content', validators = [DataRequired()])
	submit = SubmitField('Post')
