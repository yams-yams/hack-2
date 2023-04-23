from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, NumberRange, Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    year = IntegerField('Catalog Year (What Academic Year Did You Start Your Degree)', validators=[DataRequired(),NumberRange(min=2013,max=2023)])
    file = FileField('Degree Plan', validators=[Optional(strip_whitespace=True)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.') 

class RequestForm(FlaskForm):
    query = StringField('What is your question?', validators=[DataRequired()])
    submit = SubmitField('Submit')