from flask import Flask

app = Flask(__name__)

# "Oletuspolku" esim. http://example.com/  
@app.route("/")
def hello():
    return "Hei maailma!"

if __name__ == "__main__":
    # Ohjelman käynnistäminen debug-tilassa
    app.run(debug=True)