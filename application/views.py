from application import app, db
from flask import render_template

# Index-sivu
@app.route("/")
def index():
    return render_template("index.html")