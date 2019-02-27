from application import app, db
from flask import render_template
from application.recipes.models import Resepti
from datetime import date, timedelta

# Index-sivu
@app.route("/")
def index():
    # Haetaan 10 viimeisintä reseptiä...
    cursor = db.engine.execute("SELECT resepti.id as id, resepti.nimi as nimi, resepti.kuvaus as kuvaus, valmistusaika.tunti as tunti, valmistusaika.minuutti as minuutti FROM resepti LEFT JOIN valmistusaika ON valmistusaika.id = resepti.valmistusaika_id ORDER BY resepti.luotu DESC LIMIT 10")
    recipes = cursor.fetchall()
    cursor.close()

    # Haetaan 10 viimeisintä pika reseptiä (alle 15 min)...
    cursor = db.engine.execute("SELECT resepti.id as id, resepti.nimi as nimi, resepti.kuvaus as kuvaus, valmistusaika.tunti as tunti, valmistusaika.minuutti as minuutti FROM resepti LEFT JOIN valmistusaika ON valmistusaika.id = resepti.valmistusaika_id WHERE valmistusaika.tunti = 0 AND valmistusaika.minuutti <= 15 ORDER BY resepti.luotu DESC LIMIT 10")
    quick_recipes = cursor.fetchall()
    cursor.close()
    
    return render_template("index.html", recipes=recipes, quick_recipes=quick_recipes)
