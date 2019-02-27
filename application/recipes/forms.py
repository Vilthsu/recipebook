from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    name = StringField("Nimi", validators=[DataRequired()])
    recipe = TextAreaField("Valmistusohje", validators=[DataRequired()])
    description = TextAreaField("Kuvaus", validators=[DataRequired()], description="Kirjoita reseptille jokin kuvaava kuvaus")
 
    class Meta:
        csrf = False
