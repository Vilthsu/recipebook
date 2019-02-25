from application import app, db
from flask import redirect, render_template, request, url_for
from application.recipes.models import Resepti, Valmistusaika, MaaraYksikko
from application.recipes.forms import RecipeForm
from flask_login import login_required

# Kaikki reseptit
@app.route("/recipes")
@app.route("/recipes/")
def recipes_list():
    return render_template("recipes/list.html", recipes = Resepti.query.all())

# Uuden reseptin lisäys
@app.route("/recipes/new", methods=["GET", "POST"])
@login_required
def recipes_new():
    prefix = "recipe-"
    units = MaaraYksikko.query.all()

    if request.method == "GET":
        return render_template("recipes/new.html", form = RecipeForm(prefix=prefix), prefix = prefix, units = units)

    # Lyhyempi tapa etsiä kenttiä lähetetystä datasta
    data = request.form
    form = RecipeForm(data, prefix=prefix)

    if not form.validate():
        return render_template("recipes/new.html", form = form, prefix = prefix, units = units, error = "Täytä kaikki tähdellä merkityt kentät")

    # return str(data)

    # Etsi kentät ja muunna oikeaan formaattiin (esim. kokonaisluvut int, vaikkei Python ole vahvasti tyypitetty ohjelmointikieli)
    recipe_name = data[prefix + "name"].strip()
    recipe_recipe = data[prefix + "recipe"].strip()
    recipe_desc = data[prefix + "description"].strip()
    cooking_time_hours = int(data["cooking-time-hours"].strip())
    cooking_time_minutes = int(data["cooking-time-minutes"].strip())
    recipe_ingredient_total = int(data[prefix + "ingredient-total"].strip())

    # Validoi valmistusaika
    if cooking_time_hours == 0 and cooking_time_minutes == 0:
        return render_template("recipes/new.html", form = form, prefix = prefix, units = units, error = "Virheellinen valmistusaika")

    # Validoi raaka-aineiden määrä
    if recipe_ingredient_total <= 0 or not data[prefix + "ingredient-name[0]"]:
        return render_template("recipes/new.html", form = form, prefix = prefix, units = units, error = "Raaka-aineita tulee olla vähintään yksi")

    # Luodaan raaka-aineita varten muutama apumuutuja (arrayt)
    recipe_ingredient_name_ids = []
    recipe_ingredient_amounts = []
    recipe_ingredient_unit_ids = []

    # Käydään läpi lähetetyt raaka-aineet
    for i in range(0, recipe_ingredient_total - 1):
        # Etsitään jo olemassa olevan raaka-aineen nimi
        if prefix + "ingredient-name[" + str(i) + "]" in data:
            # Käsittele raaka-aineen nimi
            ingredient_name = data[prefix + "ingredient-name[" + str(i) + "]"]

            cursor = db.engine.execute("SELECT id FROM raaka_aine WHERE nimi = ? LIMIT 1", ingredient_name)
            name_rows = cursor.fetchone()
            cursor.close()

            # Tarkistetaan onko jo olemassa olevaa ID:tä (nimen osalta)
            if not name_rows:
                # ID:tä ei löytynyt -> lisätään uusi raaka-aineen nimi
                cursor = db.engine.execute("INSERT INTO raaka_aine (nimi) VALUES (?)", ingredient_name)
                
                # Koska lisätty rivi on viimeinen rivi, voidaan hakea sen ID suoraan vastauksesta
                name_id = cursor.lastrowid
                cursor.close()
            else:
                # Tallennetaan olemassa oleva ID muuttujaan name_id
                name_id = name_rows.id

            # Lisätään nimen ID
            recipe_ingredient_name_ids.append(name_id)
            
            # Käsittele raaka-aineen määrän yksikkö, jos annettu ...
            if data[prefix + "ingredient-unit[" + str(i) + "]"]:
                ingredient_unit = data[prefix + "ingredient-unit[" + str(i) + "]"]

                cursor = db.engine.execute("SELECT id FROM maara_yksikko WHERE nimi = ? LIMIT 1", ingredient_unit)
                unit_rows = cursor.fetchone()
                cursor.close()

                # Tarkistetaan onko jo olemassa olevaa ID:tä (nimen osalta)
                if not unit_rows:
                    # ID:tä ei löytynyt -> lisätään uusi raaka-aineen nimi
                    cursor = db.engine.execute("INSERT INTO maara_yksikko (nimi) VALUES (?)", ingredient_unit)
                    
                    # Koska lisätty rivi on viimeinen rivi, voidaan hakea sen ID suoraan vastauksesta
                    unit_id = cursor.lastrowid
                    cursor.close()
                else:
                    # Tallennetaan olemassa oleva ID muuttujaan name_id
                    unit_id = unit_rows.id

            else:
                # ... muulloin ei ole yksikköä eli ID 0
                unit_id = 0

            # Lisätään yksikön ID
            recipe_ingredient_unit_ids.append(name_id)

            # Käsitellään vielä määrä
            if data[prefix + "ingredient-amount[" + str(i) + "]"]:
                amount = int(data[prefix + "ingredient-amount[" + str(i) + "]"])
            else:
                amount = 0
            
            recipe_ingredient_amounts.append(amount)

    # Etsitään jo olemassa oleva valmistusaika
    cursor = db.engine.execute("SELECT id FROM valmistusaika WHERE tunti = ? AND minuutti = ? LIMIT 1", cooking_time_hours, cooking_time_minutes)

    # Haetaan tiedot
    cooking_time = cursor.fetchone()

    # Suljetaan tietokantakysely
    cursor.close()
    
    # Tarkistetaan onko jo olemassa olevaa ID:tä
    if not cooking_time:
        # ID:tä ei löytynyt -> lisätään uusi valmistusaika
        cursor = db.engine.execute("INSERT INTO valmistusaika (tunti, minuutti) VALUES (?, ?)", cooking_time_hours, cooking_time_minutes)
        
        # Koska lisätty rivi on viimeinen rivi, voidaan hakea sen ID suoraan vastauksesta
        cooking_time_id = cursor.lastrowid
        cursor.close()
    else:
        # Tallennetaan olemassa oleva ID muuttujaan cooking_time_id
        cooking_time_id = cooking_time.id

    # Lisätään uusi resepti
    cursor = db.engine.execute("INSERT INTO resepti (nimi, valmistusaika_id, valmistusohje, kuvaus) VALUES (?, ?, ?, ?)", recipe_name, cooking_time_id, recipe_recipe, recipe_desc)

    new_recipe_id = cursor.lastrowid
    cursor.close()
    
    # Lisää raaka-aineiden liitostaulun data
    for i in range(0, len(recipe_ingredient_name_ids)):
        cursor = db.engine.execute("INSERT INTO resepti_raaka_aine (resepti_id, raaka_aine_id, maara, maara_yksikko_id) VALUES (?, ?, ?, ?)", new_recipe_id, recipe_ingredient_name_ids[i], recipe_ingredient_amounts[i], recipe_ingredient_unit_ids[i])

    # TODO: uudelleenohjaus reseptin sivulle
    return redirect(url_for("recipes_list"))

# Reseptisivu
@app.route("/recipes/<recipe_id>", methods=["GET"])
def recipes_view(recipe_id):
    recipe = Resepti.query.get(recipe_id)
    return render_template("recipes/view.html", recipe=recipe)