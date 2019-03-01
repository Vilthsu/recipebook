from application import app, bcrypt, db
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from application.auth.models import Kayttaja
from application.auth.forms import LoginForm, RegistrationForm

@app.route("/auth/login", methods = ["GET", "POST"])
def login():
    # Halutessaan voi käyttää etuliitettä (prefix)
    prefix = "login-"
    
    # Renderöidään GET-pyynnössä lomake ilman dataa
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm(prefix=prefix))

    # Lomakkeen data
    data = request.form
    form = LoginForm(data, prefix=prefix)

    # Tallennetaan lähetetyt tiedot lyhyempiin muuttujiin kästtelyä varten
    email = data[prefix + "email"].strip()
    passwd = data[prefix + "password"].strip()

    # Haetaan sähköpostiin liittyvän käyttäjän tiedot. Tarvitsemme aluksi salasanan hashin.
    stmt = text("SELECT salasana FROM kayttaja WHERE sahkopostiosoite = :email LIMIT 1").params(email=email)
    cursor = db.engine.execute(stmt)
    
    # Haetaan tulos
    result = cursor.fetchone()
    cursor.close()

    # Jos salasana hashia ei löytynyt, tarkoittaa se samalla sitä ettei käyttäjää ole olemassa
    if not result:
        return render_template("auth/loginform.html", form=form, error="Käyttäjää ei löytynyt")

    # Halutessaan tämän voisi jättää pois mutta säilytetään selkeyden vuoksi
    passwd_hash = result.salasana

    # Tarkistataan hash
    if not bcrypt.check_password_hash(passwd_hash, passwd):
        return render_template("auth/loginform.html", form=form, error="Käyttäjää ei löytynyt")

    # Käyttäjä sisäänkirjaus
    user = Kayttaja.query.filter_by(sahkopostiosoite=email, salasana=passwd_hash).first()

    # Kenties turha tarkistus...
    if not user:
        return render_template("auth/loginform.html", form=form, error="Käyttäjää ei löytynyt")

    login_user(user)

    # Kaikki kunnossa -> palautetaan käyttäjä etusivulle
    return redirect(url_for("index"))

@app.route("/auth/registration", methods = ["GET", "POST"])
def registratation():
    # Halutessaan voi käyttää etuliitettä (prefix)
    prefix = "registratation-"

    # Renderöidään GET-pyynnössä lomake ilman dataa
    if request.method == "GET":
        return render_template("auth/registrationform.html", form=RegistrationForm(prefix=prefix))

    # Lomakkeen data
    data = request.form
    form = RegistrationForm(data, prefix=prefix)
    
    # Validoinnit
    if not form.validate():
        return render_template("auth/registrationform.html", form=form, error="Täytä kaikki vaaditut kentät")

    # Tallennetaan lähetetyt tiedot lyhyempiin muuttujiin kästtelyä varten
    email = data[prefix + "email"].strip()
    firstname = data[prefix + "firstname"].strip()
    lastname = data[prefix + "lastname"].strip()
    pass1 = data[prefix + "password"].strip()
    pass2 = data[prefix + "password2"].strip()

    # Salasanan tulee olla vähintään 8 merkkiä pitkä
    # TODO: vahvista väh. 1 iso & 1 pienikirjain + 1 numero
    if len(pass1) < 8:
        return render_template("auth/registrationform.html", form=form, error="Salasana on liian lyhyt")
    
    # Salasanojen tulee täsmätä
    if pass1 != pass2:
        return render_template("auth/registrationform.html", form=form, error="Salasanat eivät täsmää")

    # Tarkistetaan onko sähköpostiosoite käytössä
    cursor = db.engine.execute("SELECT COUNT(*) as maara FROM kayttaja WHERE sahkopostiosoite = ?;", email)
    
    # Haetaan tulos
    count = cursor.fetchone()
    cursor.close()

    # Mikäli count.maara on suurempi kuin 0,
    # sähköpostiosoite on jo rekisteröity ja
    # ohjataan käyttäjä takaisin lomakkeeseen virheviestin kera.
    if count.maara > 0:
        return render_template("auth/registrationform.html", form=form, error="Syöttämäsi sähköpostiosoite on jo käytössä")

    # Koska emme halua tallentaa salasanaa selkokielisenä (plain text),
    # tallennetaan salasanan hash tietokantaan
    pass_hash = bcrypt.generate_password_hash(pass1)

    # Kaikki kunnossa, tallennetaan käyttäjä tietokantaan (käyttäjänimi on toistaiseksi tyhjä, TODO: generoi käyttäjänimi / pyydä käyttäjältä)
    cursor = db.engine.execute("INSERT INTO kayttaja (sahkopostiosoite, salasana, etunimi, sukunimi) VALUES (?, ?, ?, ?);", email, pass_hash, firstname, lastname)
    cursor.close()

    # Uudelleenohjataan käyttäjä kirjautumissivulle 
    return redirect(url_for("login") + "?from=registration&registration=ok")

@app.route("/auth/logout")
def logout():
    logout_user()
    return redirect(url_for("index") + "?logout=ok")
