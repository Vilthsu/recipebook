from application import app, db
from flask import redirect, render_template, request, url_for
from application.recipes.models import Resepti, Valmistusaika
from application.recipes.forms import RecipeForm

# Kaikki reseptit
@app.route("/recipes")
@app.route("/recipes/")
def recipes_list():
    return render_template("recipes/list.html", recipes = Resepti.query.all())

# Uuden reseptin lisäys
@app.route("/recipes/new", methods=["GET"])
def recipes_new():
    return render_template("recipes/new.html", form = RecipeForm(prefix="recipe-"))

@app.route("/recipes/new", methods=["POST"])
def recipes_create():
    # Lyhyempi tapa etsiä kenttiä lähetetystä datasta
    data = request.form
    form = RecipeForm(data, prefix="recipe-")

    if not form.validate():
        return render_template("recipes/new.html", form = form)

    # Etsi kentät ja muunna oikeaan formaattiin (esim. kokonaisluvut int, vaikkei Python ole vahvasti tyypitetty ohjelmointikieli)
    recipe_name = data["recipe-name"]
    recipe_recipe = data["recipe-recipe"]
    recipe_desc = data["recipe-description"]
    cooking_time_hours = int(data["cooking-time-hours"])
    cooking_time_minutes = int(data["cooking-time-minutes"])

    # Validoi arvot, arvojen pituus pitää olla suurempi kuin nolla (0)
    if len(recipe_name) == 0 or len(recipe_recipe) == 0 or len(recipe_desc) == 0:
        return render_template("recipes/new.html", form = form, error = "Täytä kaikki tähdellä merkityt kentät")

    # Validoi valmistusaika
    if cooking_time_hours == None or cooking_time_minutes == None or (cooking_time_hours == 0 and cooking_time_minutes == 0):
        return render_template("recipes/new.html", form = form, error = "Virheellinen valmistusaika")

    # Etsitään jo olemassa oleva valmistusaika
    cursor = db.engine.execute("SELECT id FROM valmistusaika WHERE tunti = ? AND minuutti = ? LIMIT 1", cooking_time_hours, cooking_time_minutes)
    
    # Haetaan rivit arrayna
    cooking_times = cursor.fetchall()

    # Suljetaan tietokantakysely
    cursor.close()
    
    # Tarkistetaan onko jo olemassa olevaa ID:tä
    if len(cooking_times) == 0:
        # ID:tä ei löytynyt -> lisätään uusi valmistusaika
        cursor = db.engine.execute("INSERT INTO valmistusaika (tunti, minuutti) VALUES (?, ?)", cooking_time_hours, cooking_time_minutes)
        
        # Koska lisätty rivi on viimeinen rivi, voidaan hakea sen ID suoraan vastauksesta
        cooking_time_id = cursor.lastrowid
        cursor.close()
    else:
        # Tallennetaan olemassa oleva ID muuttujaan cooking_time_id
        cooking_time_id = cooking_times[0].id

    # Lisätään uusi resepti
    cursor = db.engine.execute("INSERT INTO resepti (nimi, valmistusaika_id, valmistusohje, kuvaus) VALUES (?, ?, ?, ?)", recipe_name, cooking_time_id, recipe_recipe, recipe_desc)
    
    # TODO: uudelleenohjaus
    new_recipe_id = cursor.lastrowid
    cursor.close()
    return redirect(url_for("recipes_list"))