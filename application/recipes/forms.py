from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    name = StringField("Nimi", validators=[DataRequired()])
    recipe = TextAreaField("Valmistusohje", validators=[DataRequired()])
    description = TextAreaField("Kuvaus", validators=[DataRequired()])
 
    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    email = StringField("Sähköpostiosoite")
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False
