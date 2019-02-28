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
    button = "Lisää resepti"
    form_action = url_for('recipes_new')
    units = MaaraYksikko.query.all()

    if request.method == "GET":
        return render_template("recipes/form.html", form = RecipeForm(prefix=prefix), prefix = prefix, units = units, title = title, form_action = form_action, button=button)

    # Lyhyempi tapa etsiä kenttiä lähetetystä datasta
    data = request.form
    form = RecipeForm(data, prefix=prefix)

    # Tallennetaan kustomoitujen kenttien dataa ja palautetaan se lomakkeeseen
    saved_data = {}

    if "cooking-time-hours" in data and data["cooking-time-hours"]:
        cooking_time_hours = int(data["cooking-time-hours"].strip())
        saved_data["cooking-time-hours"] = cooking_time_hours

    if "cooking-time-minutes" in data and data["cooking-time-minutes"]:
        cooking_time_minutes = int(data["cooking-time-minutes"].strip())
        saved_data["cooking-time-minutes"] = cooking_time_minutes

    if not form.validate():
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, default_data = saved_data, button=button, error = "Täytä kaikki tähdellä merkityt kentät")

    # Etuliite raaka-aine-tiedoille
    ingredient_prefix = prefix + 'ingredient-'

    # Etsi kentät ja muunna oikeaan formaattiin (esim. kokonaisluvut int, vaikkei Python ole vahvasti tyypitetty ohjelmointikieli)
    recipe_name = data[prefix + "name"].strip()
    recipe_recipe = data[prefix + "recipe"].strip()
    recipe_desc = data[prefix + "description"].strip()
    recipe_ingredient_total = int(data[ingredient_prefix + "total"].strip())

    # Validoi valmistusaika
    if not validateCookingTime(cooking_time_hours, cooking_time_minutes):
        saved_data["cooking-time-hours"] = ""
        saved_data["cooking-time-minutes"] = ""
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, default_data = saved_data, button=button, error = "Virheellinen valmistusaika")

    # Etuliite raaka-aine-tiedoille
    ingredient_prefix = prefix + 'ingredient-'

    # Validoi raaka-aineiden määrä
    if not validateIngredients(data, recipe_ingredient_total, ingredient_prefix + "name[0]"):
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, default_data = saved_data, button=button, error = "Raaka-aineita tulee olla vähintään yksi")

    # Käsitellään raaka-aineet ...
    recipe_ingredients = add_recipe_ingredients(data, recipe_ingredient_total, ingredient_prefix + 'name', ingredient_prefix + 'amount', ingredient_prefix + 'unit')

    # ... vastauksena saadaan ID:t raaka-aineiden nimille ja määrien yksiköille sekä raaka-aineiden määrät 
    recipe_ingredient_name_ids = recipe_ingredients.name_ids
    recipe_ingredient_amounts = recipe_ingredients.amounts
    recipe_ingredient_unit_ids = recipe_ingredients.unit_ids

    # Valmistusajan käsittely
    cooking_time_id = get_cooking_time_id(cooking_time_hours, cooking_time_minutes)

    # Lisätään uusi resepti
    cursor = db.engine.execute("INSERT INTO resepti (nimi, valmistusaika_id, valmistusohje, kuvaus, kayttaja_id) VALUES (?, ?, ?, ?, ?)", recipe_name, cooking_time_id, recipe_recipe, recipe_desc, current_user.get_id())

    new_recipe_id = cursor.lastrowid
    cursor.close()
    
    # Lisää raaka-aineiden liitostaulun data
    for i in range(0, len(recipe_ingredient_name_ids)):
        cursor = db.engine.execute("INSERT INTO resepti_raaka_aine (resepti_id, raaka_aine_id, maara, maara_yksikko_id) VALUES (?, ?, ?, ?)", new_recipe_id, recipe_ingredient_name_ids[i], recipe_ingredient_amounts[i], recipe_ingredient_unit_ids[i])
        cursor.close()

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
    button = "Tallenna resepti"
    form_action = url_for('recipes_edit', recipe_id=recipe.id)
    units = MaaraYksikko.query.all()

    if not recipe:
        return "Error 404: Not found"

    if recipe.kayttaja_id is not current_user.get_id():
        return render_template("auth/unauthorized.html")

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
    
    for ingredient in ingredients:
        if ingredient.raaka_aine:
            raaka_aine = ingredient.raaka_aine.nimi
            maara = ingredient.maara
            
            if maara == 0:
                maara = ""

            if ingredient.maara_yksikko:
                yksikko = ingredient.maara_yksikko.nimi
            else:
                yksikko = ""
            
            data[prefix + "ingredient-name"].append(raaka_aine)
            data[prefix + "ingredient-amount"].append(maara)
            data[prefix + "ingredient-unit"].append(yksikko)

    default_data = {}
    default_data["name"] = recipe.nimi
    default_data["recipe"] = recipe.valmistusohje
    default_data["description"] = recipe.kuvaus

    # Lomakkeen rakentaminen, lomake-olio
    form = RecipeForm(data=default_data, prefix=prefix, button=button)
    form.name.default = recipe.nimi
    form.description.default = recipe.kuvaus
    form.recipe.default = recipe.valmistusohje

    ingredient_count = len(data[prefix + "ingredient-name"])

    if request.method == "GET":
        return render_template("recipes/form.html", form = form, prefix = prefix, id = recipe.id, title = title, form_action = form_action, units = units, default_data = data, button=button, ingredient_count = ingredient_count)
    
    # POST-pyyntö:
    data = request.form
    return recipes_edit_post(data, prefix, recipe_id, title, form_action, units, data, button)

def recipes_edit_post(data, prefix, recipe_id, title, form_action, units, default_data, button):
    form = RecipeForm(data, prefix=prefix, button=button)

    # Validoi data
    if not form.validate():
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, default_data = default_data, button=button, error = "Täytä kaikki tähdellä merkityt kentät")

    # Etuliite raaka-aine-tiedoille
    ingredient_prefix = prefix + 'ingredient-'

    # Etsi kentät ja muunna oikeaan formaattiin (esim. kokonaisluvut int, vaikkei Python ole vahvasti tyypitetty ohjelmointikieli)
    recipe_name = data[prefix + "name"].strip()
    recipe_recipe = data[prefix + "recipe"].strip()
    recipe_desc = data[prefix + "description"].strip()
    cooking_time_hours = int(data["cooking-time-hours"].strip())
    cooking_time_minutes = int(data["cooking-time-minutes"].strip())
    recipe_ingredient_total = int(data[ingredient_prefix + "total"].strip())

    # Validoi valmistusaika
    if not validateCookingTime(cooking_time_hours, cooking_time_minutes):
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, default_data = default_data, button=button, error = "Virheellinen valmistusaika")

    # Validoi raaka-aineiden määrä
    if not validateIngredients(data, recipe_ingredient_total, ingredient_prefix + "name[0]"):
        return render_template("recipes/form.html", form = form, prefix = prefix, units = units, title = title, form_action = form_action, default_data = default_data, button=button, error = "Raaka-aineita tulee olla vähintään yksi")

    # Käsitellään raaka-aineet ...
    recipe_ingredients = add_recipe_ingredients(data, recipe_ingredient_total, ingredient_prefix + 'name', ingredient_prefix + 'amount', ingredient_prefix + 'unit')

    # ... vastauksena saadaan ID:t raaka-aineiden nimille ja määrien yksiköille sekä raaka-aineiden määrät 
    recipe_ingredient_name_ids = recipe_ingredients.name_ids
    recipe_ingredient_amounts = recipe_ingredients.amounts
    recipe_ingredient_unit_ids = recipe_ingredients.unit_ids

    # Valmistusajan käsittely
    cooking_time_id = get_cooking_time_id(cooking_time_hours, cooking_time_minutes)
    
    # Poistetaan vanhat raaka-aineet
    cursor = db.engine.execute("DELETE FROM resepti_raaka_aine WHERE resepti_id = ?", recipe_id)
    cursor.close()

    # Päivitetään reseptin tiedot
    cursor = db.engine.execute("UPDATE resepti SET nimi = ?, kuvaus = ?, valmistusohje = ? WHERE id = ?", recipe_name, recipe_desc, recipe_recipe, recipe_id)
    cursor.close()

    # Lisää raaka-aineiden liitostaulun data
    for i in range(0, len(recipe_ingredient_name_ids)):
        cursor = db.engine.execute("INSERT INTO resepti_raaka_aine (resepti_id, raaka_aine_id, maara, maara_yksikko_id) VALUES (?, ?, ?, ?)", recipe_id, recipe_ingredient_name_ids[i], recipe_ingredient_amounts[i], recipe_ingredient_unit_ids[i])
        cursor.close()

    return redirect(url_for("recipes_view", recipe_id = recipe_id) + "?status=updated")

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

def get_cooking_time_id(hours, minutes):
    # Etsitään jo olemassa oleva valmistusaika
    cursor = db.engine.execute("SELECT id FROM valmistusaika WHERE tunti = ? AND minuutti = ? LIMIT 1", hours, minutes)

    # Haetaan tiedot
    cooking_time = cursor.fetchone()

    # Suljetaan tietokantakysely
    cursor.close()
    
    # Tarkistetaan onko jo olemassa olevaa ID:tä
    if not cooking_time:
        # ID:tä ei löytynyt -> lisätään uusi valmistusaika
        cursor = db.engine.execute("INSERT INTO valmistusaika (tunti, minuutti) VALUES (?, ?)", hours, minutes)
        
        # Koska lisätty rivi on viimeinen rivi, voidaan hakea sen ID suoraan vastauksesta
        cooking_time_id = cursor.lastrowid
        cursor.close()
    else:
        # Tallennetaan olemassa oleva ID muuttujaan cooking_time_id
        cooking_time_id = cooking_time.id

    return cooking_time_id

def get_unit_id(unit_name):
    cursor = db.engine.execute("SELECT id FROM maara_yksikko WHERE nimi = ? LIMIT 1", unit_name)
    unit_rows = cursor.fetchone()
    cursor.close()

    # Tarkistetaan onko jo olemassa olevaa ID:tä (nimen osalta)
    if not unit_rows:
        # ID:tä ei löytynyt -> lisätään uusi raaka-aineen nimi
        cursor = db.engine.execute("INSERT INTO maara_yksikko (nimi) VALUES (?)", unit_name)
        
        # Koska lisätty rivi on viimeinen rivi, voidaan hakea sen ID suoraan vastauksesta
        unit_id = cursor.lastrowid
        cursor.close()
    else:
        # Tallennetaan olemassa oleva ID muuttujaan name_id
        unit_id = unit_rows.id

    return unit_id

def add_recipe_ingredients(data, recipe_ingredient_total, ingredient_name_arr_index, ingredient_amount_arr_index, ingredient_unit_arr_index):
    # Luodaan raaka-aineita varten muutama apumuutuja (arrayt)
    recipe_ingredient_name_ids = []
    recipe_ingredient_amounts = []
    recipe_ingredient_unit_ids = []

    # Käydään läpi lähetetyt raaka-aineet
    for i in range(0, recipe_ingredient_total):

        i_str = str(i)
        # Käytetään lyhyempiä muuttujien nimeä
        ingredient_name_index = ingredient_name_arr_index + "[" + i_str + "]"
        ingredient_amount_index = ingredient_amount_arr_index + "[" + i_str + "]"
        ingredient_unit_index = ingredient_unit_arr_index + "[" + i_str + "]"
        
        # Etsitään jo olemassa olevan raaka-aineen nimi
        if ingredient_name_index in data:
            # Käsittele raaka-aineen nimi
            ingredient_name = data[ingredient_name_index]

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

            if name_id in recipe_ingredient_name_ids:
                continue
            
            # Lisätään nimen ID
            recipe_ingredient_name_ids.append(name_id)
            
            # Käsittele raaka-aineen määrän yksikkö, jos annettu ...
            if ingredient_unit_index in data:
                if data[ingredient_unit_index]:
                    ingredient_unit = data[ingredient_unit_index]

                    unit_id = get_unit_id(ingredient_unit)
                else:
                    unit_id = 0
            else:
                # ... muulloin ei ole yksikköä eli ID 0
                unit_id = 0

            # Lisätään yksikön ID
            recipe_ingredient_unit_ids.append(unit_id)

            # Käsitellään vielä määrä
            if ingredient_amount_index in data:
                if data[ingredient_amount_index]:
                    amount = int(data[ingredient_amount_index])
                else:
                    amount = 0
            else:
                amount = 0
            
            # Validoidaan määrä
            if amount < 0:
                amount = 0

            recipe_ingredient_amounts.append(amount)

    return_obj = IntegredientResult()

    return_obj.name_ids = recipe_ingredient_name_ids
    return_obj.amounts = recipe_ingredient_amounts
    return_obj.unit_ids = recipe_ingredient_unit_ids

    return return_obj

class IntegredientResult():
    name_ids = []
    amounts = []
    unit_ids = []

def validateCookingTime(cooking_time_hours, cooking_time_minutes):
    if cooking_time_hours < 0 or cooking_time_minutes < 0:
        return False

    if cooking_time_hours == 0 and cooking_time_minutes == 0:
        return False

    return True

def validateIngredients(data, total, index):
    if total <= 0:
        return False

    if index not in data:
        return False

    if not data[index]:
        return False

    return True
