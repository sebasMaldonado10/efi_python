from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired

class RegistroForm(FlaskForm):
    username = StringField('usuario', validators=[DataRequired()]) #campos requeridos
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ComentarioForm(FlaskForm):
    texto = TextAreaField('texto', validators=[DataRequired()])


