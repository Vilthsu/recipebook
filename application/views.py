from application import app, db
from flask import render_template
from application.recipes.models import Resepti

# Index-sivu
@app.route("/")
def index():
    # Haetaan 10 viimeisintä reseptiä...
    recipes = Resepti.query.order_by(Resepti.luotu.desc()).limit(10).all()
    return render_template("index.html", recipes=recipes)
