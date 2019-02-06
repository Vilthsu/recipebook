from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import Kayttaja
from application.auth.forms import LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())