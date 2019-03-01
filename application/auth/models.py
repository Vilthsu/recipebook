from application import db

class Kayttaja(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    kayttajatunnus = db.Column(db.String(50), nullable=True)
    salasana = db.Column(db.String(50), nullable=False)
    etunimi = db.Column(db.String(20), nullable=False)
    sukunimi = db.Column(db.String(20), nullable=False)
    sahkopostiosoite = db.Column(db.String(50), nullable=False)
    rekisteroitynyt = db.Column(db.DateTime, default=db.func.current_timestamp())
    muokattu = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, kayttajatunnus, etunimi, sukunimi, sahkopostiosoite, rekisteroitynyt, muokattu):
        self.kayttajatunnus = kayttajatunnus
        self.etunimi = etunimi
        self.sukunimi = sukunimi
        self.sahkopostiosoite = sahkopostiosoite
        self.rekisteroitynyt = rekisteroitynyt
        self.muokattu = muokattu
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_fullname(self):
        if self.etunimi and self.sukunimi:
            return self.etunimi + " " + self.sukunimi

        return self.kayttajatunnus