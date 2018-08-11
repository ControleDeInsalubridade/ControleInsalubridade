from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    CPF = StringField('Username', validators=[DataRequired()])
    Senha = PasswordField('Password', validators=[DataRequired()])
    Lembrar = BooleanField('Remember Me')
    submit = SubmitField('Sign In')