from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.recipes import models
from application.recipes import views

from application.auth import models
from application.auth import views

# Kirjautumiseen tarvittavat moduulit ym.
from application.auth.models import Kayttaja
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

# Login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Sinun tulee kirjautua sisään ennen tälle sivulle siirtymistä."

@login_manager.user_loader
def load_user(user_id):
    return Kayttaja.query.get(user_id)

db.create_all()
