
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from models import User
from passlib.hash import pbkdf2_sha256

def invalid_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
            
        raise ValidationError("Username or Password is incorrect!!")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or Password is incorrect!!")
    
        
class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(),Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label ='Password',validators=[DataRequired(),Length(min=6, max=16)])
    confirm_password = PasswordField(label ='Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(label='Sign Up')
    
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            
            raise ValidationError("Someone else has taken this username!!")
            
    def validate_email(self, email):
        email_object = User.query.filter_by(email=email.data).first()
        if email_object:
            
            raise ValidationError("This email exists. Please provide an alternative !!")

class LoginForm(FlaskForm):
    
    username = StringField(label='Username', validators=[DataRequired(),Length(min=3, max=20)])
    password = PasswordField(label ='Password',validators=[DataRequired(), invalid_credentials])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Login')