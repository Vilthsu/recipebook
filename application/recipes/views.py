from application import app, db
from flask import redirect, render_template, request, url_for
from application.recipes.models import Resepti, Valmistusaika, MaaraYksikko, ReseptiRaakaAine
from application.recipes.forms import RecipeForm
from flask_login import login_required, current_user

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
    title = "Lisää resepti"
    form_action = url_for('recipes_new')
    units = MaaraYksikko.query.all()

    if request.method == "GET":
        return render_template("recipes/form.html", form = RecipeForm(prefix=prefix), prefix = prefix, units = units, title = title, form_action = form_action)

    # Lyhyempi tapa etsiä kenttiä lähetetystä datasta
    data = request.form
    form = RecipeForm(data, prefix=prefix)

    if not form.validate():
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, error = "Täytä kaikki tähdellä merkityt kentät")

    # Etsi kentät ja muunna oikeaan formaattiin (esim. kokonaisluvut int, vaikkei Python ole vahvasti tyypitetty ohjelmointikieli)
    recipe_name = data[prefix + "name"].strip()
    recipe_recipe = data[prefix + "recipe"].strip()
    recipe_desc = data[prefix + "description"].strip()
    cooking_time_hours = int(data["cooking-time-hours"].strip())
    cooking_time_minutes = int(data["cooking-time-minutes"].strip())
    recipe_ingredient_total = int(data[prefix + "ingredient-total"].strip())

    # Validoi valmistusaika
    if cooking_time_hours == 0 and cooking_time_minutes == 0:
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, error = "Virheellinen valmistusaika")

    # Validoi raaka-aineiden määrä
    if recipe_ingredient_total <= 0 or not data[prefix + "ingredient-name[0]"]:
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, error = "Raaka-aineita tulee olla vähintään yksi")

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
            recipe_ingredient_unit_ids.append(unit_id)

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
    cursor = db.engine.execute("INSERT INTO resepti (nimi, valmistusaika_id, valmistusohje, kuvaus, kayttaja_id) VALUES (?, ?, ?, ?, ?)", recipe_name, cooking_time_id, recipe_recipe, recipe_desc, current_user.get_id())

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

    # Raaka-aineiden hakeminen
    if recipe:
        # SELECT * FROM resepti_raaka_aine WHERE resepti_id = {recipe_id},
        # toteutettu SQLAlchemyn tarjoamalla API:lla, jotta saadaan käyttöön 
        ingredients = ReseptiRaakaAine.query.filter_by(resepti_id=recipe_id).all()

        owner = current_user.get_id() == recipe.kayttaja.id

    else:
        owner = False

    return render_template("recipes/view.html", recipe=recipe, owner = owner, ingredients = ingredients)

# Reseptin muokkaussivu
@login_required
@app.route("/recipes/<recipe_id>/edit", methods=["GET", "POST"])
def recipes_edit(recipe_id):
    recipe = Resepti.query.get(recipe_id)
    prefix = "recipe-"
    title = "Muokkaa reseptiä"
    form_action = url_for('recipes_edit', recipe_id=recipe.id)
    units = MaaraYksikko.query.all()

    if not recipe:
        return "Error 404: Not found"

    if recipe.kayttaja_id is not current_user.get_id():
        return render_template("auth/unauthorized.html")

    if request.method == "GET":
        # Raaka-aineiden hakeminen
        # SELECT * FROM resepti_raaka_aine WHERE resepti_id = {recipe_id},
        # toteutettu SQLAlchemyn tarjoamalla API:lla, jotta saadaan käyttöön 
        ingredients = ReseptiRaakaAine.query.filter_by(resepti_id=recipe_id).all()

        # Lomakkeen rakentaminen, data
        data = {}
        data[prefix + "name"] = recipe.nimi
        data[prefix + "recipe"] = recipe.valmistusohje
        data[prefix + "description"] = recipe.kuvaus
        data["cooking-time-hours"] = recipe.valmistusaika.tunti
        data["cooking-time-minutes"] = recipe.valmistusaika.minuutti

        data[prefix + "ingredient-name"] = []
        data[prefix + "ingredient-amount"] = []
        data[prefix + "ingredient-unit"] = []
        
        i = 0
        for ingredient in ingredients:
            if ingredient.raaka_aine:
                raaka_aine = ingredient.raaka_aine.nimi
                maara = ingredient.maara
                
                if ingredient.maara_yksikko:
                    yksikko = ingredient.maara_yksikko.nimi
                else:
                    yksikko = ""
                
                data[prefix + "ingredient-name"].append(raaka_aine)
                data[prefix + "ingredient-amount"].append(maara)
                data[prefix + "ingredient-unit"].append(yksikko)

                i += 1

        # Lomakkeen rakentaminen, lomake-olio
        form = RecipeForm(prefix=prefix)

        return render_template("recipes/form.html", form = form, id = recipe.id, title = title, form_action = form_action, units = units, data = data)
    
    return ""

@login_required
@app.route("/recipes/<recipe_id>/delete", methods=["GET"])
def recipes_delete(recipe_id):
    recipe = Resepti.query.get(recipe_id)

    if not recipe:
        return "Error 404: Not found"

    if recipe.kayttaja_id is not current_user.get_id():
        return render_template("auth/unauthorized.html")
    
    cursor = db.engine.execute("DELETE FROM resepti WHERE id = ?", recipe.id)
    cursor = db.engine.execute("DELETE FROM resepti_raaka_aine WHERE resepti_id = ?", recipe.id)
    cursor.close()
    
    return redirect(url_for("recipes_list") + "?deleted=true")
