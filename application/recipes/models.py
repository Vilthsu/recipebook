from application import db
        
class Valmistusaika(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tunti = db.Column(db.Integer, nullable=False)
    minuutti = db.Column(db.Integer, nullable=False)

    def __init__(self, tunti, minuutti):
        self.tunti = tunti
        self.minuutti = minuutti

class MaaraYksikko(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(20), nullable=False)
    ryhma_nro = db.Column(db.Integer, nullable=False)

    def __init__(self, nimi, ryhma_nro):
        self.nimi = nimi
        self.ryhma_nro = ryhma_nro

class Resepti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(255), nullable=False)
    valmistusaika_id = db.Column(db.Integer, db.ForeignKey('valmistusaika.id'))
    valmistusohje = db.Column(db.String(), nullable=False)
    kuvaus = db.Column(db.String(255), nullable=False)
    luotu = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Vierasavaimet
    valmistusaika = db.relationship('Valmistusaika', foreign_keys=valmistusaika_id)

    def __init__(self, nimi, valmistusaika_id, valmistusohje, kuvaus):
        self.nimi = nimi
        self.valmistusaika_id = valmistusaika_id
        self.valmistusohje = valmistusohje
        self.kuvaus = kuvaus

class RaakaAine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)

    def __init__(self, nimi):
        self.nimi = nimi

class ReseptiRaakaAine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resepti_id = db.Column(db.Integer, db.ForeignKey('resepti.id'))
    raaka_aine_id = db.Column(db.Integer, db.ForeignKey('raaka_aine.id'))
    maara = db.Column(db.Numeric(precision=3, asdecimal=False, decimal_return_scale=None), nullable=False)
    maara_yksikko_id = db.Column(db.Integer, db.ForeignKey('maara_yksikko.id'))

    # Vierasavaimet
    resepti = db.relationship('Resepti', foreign_keys=resepti_id)
    raaka_aine = db.relationship('RaakaAine', foreign_keys=raaka_aine_id)
    maarayksikko = db.relationship('MaaraYksikko', foreign_keys=maara_yksikko_id)

    def __init__(self, maara, maara_yksikko_id):
        self.maara = maara
        self.maara_yksikko_id = maara_yksikko_id
