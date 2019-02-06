from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    name = StringField("Nimi", validators=[DataRequired()])
    recipe = TextAreaField("Valmistusohje", validators=[DataRequired()])
    desc = TextAreaField("Kuvaus", validators=[DataRequired()])
 
    class Meta:
        csrf = False