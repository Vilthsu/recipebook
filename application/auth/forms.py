from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField("Sähköpostiosoite", validators=[DataRequired()])
    password = PasswordField("Salasana", validators=[DataRequired()])
  
    class Meta:
        csrf = False

class RegistrationForm(FlaskForm):
    email = EmailField("Sähköpostiosoite", validators=[DataRequired()])
    # TODO: username = StringField("Käyttäjänimi", validators=[DataRequired()], description="Välilyönnit ym. eivät ole sallittuja merkkejä.")
    firstname = StringField("Etunimi", validators=[DataRequired()])
    lastname = StringField("Sukunimi", validators=[DataRequired()])
    password = PasswordField("Salasana", validators=[DataRequired()], description="Salasanan tulee olla vähintään 8 merkkiä pitkä.")
    password2 = PasswordField("Salasana uudelleen", validators=[DataRequired()])
  
    class Meta:
        csrf = False
