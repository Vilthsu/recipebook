from application import db

class Resepti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(255), nullable=False)
    valmistusaika_id = db.Column(db.Integer, db.ForeignKey('valmistusaika.id'))
    valmistusohje = db.Column(db.String(), nullable=False)
    kuvaus = db.Column(db.String(255), nullable=False)
    
    # Vierasavaimet
    valmistusaika = db.relationship('Valmistusaika', foreign_keys=valmistusaika_id)

    def __init__(self, name):
        self.name = name
        
class Valmistusaika(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tunti = db.Column(db.Integer, nullable=False)
    minuutti = db.Column(db.Integer, nullable=False)

    def __init__(self, tunti, minuutti):
        self.tunti = tunti
        self.minuutti = minuutti