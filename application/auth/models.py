from application import db

class Kayttaja(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    kayttajatunnus = db.Column(db.String(50), nullable=False)
    salasana = db.Column(db.String(50), nullable=False)
    etunimi = db.Column(db.String(50), nullable=False)
    sukunimi = db.Column(db.String(50), nullable=False)
    sahkopostiosoite = db.Column(db.String(100), nullable=False)
    rekisteroitynyt = db.Column(db.DateTime, default=db.func.current_timestamp())
    muokattu = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, nimi, kayttajatunnus, salasana, etunimi, sukunimi, sahkopostiosoite):
        self.nimi = nimi
        self.kayttajatunnus = kayttajatunnus
        self.salasana = salasana
        self.etunimi = etunimi
        self.sukunimi = sukunimi
        self.sahkopostiosoite = sahkopostiosoite
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True