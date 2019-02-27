# Tietokantakyselyjä
## Sivuilla olevat tietokantakyselyt
Raaka-aineet ja valmistusaika
```
SELECT id FROM maara_yksikko WHERE nimi = ? LIMIT 1
INSERT INTO maara_yksikko (nimi) VALUES (?)

SELECT id FROM valmistusaika WHERE tunti = ? AND minuutti = ? LIMIT 
INSERT INTO valmistusaika (tunti, minuutti) VALUES (?, ?)
```

Reseptin lisäys
```
INSERT INTO resepti (nimi, valmistusaika_id, valmistusohje, kuvaus, kayttaja_id) VALUES (?, ?, ?, ?, ?)
INSERT INTO resepti_raaka_aine (resepti_id, raaka_aine_id, maara, maara_yksikko_id) VALUES (?, ?, ?, ?)
```

Viimeisimmät reseptit (max 10 kpl)
```
SELECT resepti.id as id, resepti.nimi as nimi, resepti.kuvaus as kuvaus, valmistusaika.tunti as tunti, valmistusaika.minuutti as minuutti FROM resepti LEFT JOIN valmistusaika ON valmistusaika.id = resepti.valmistusaika_id ORDER BY resepti.luotu DESC LIMIT 10
```

Viimeisimmät alle 15 min "pika"reseptit (max 10 kpl)
```
SELECT resepti.id as id, resepti.nimi as nimi, resepti.kuvaus as kuvaus, valmistusaika.tunti as tunti, valmistusaika.minuutti as minuutti FROM resepti LEFT JOIN valmistusaika ON valmistusaika.id = resepti.valmistusaika_id WHERE valmistusaika.tunti = 0 AND valmistusaika.minuutti <= 15 ORDER BY resepti.luotu DESC LIMIT 10
```

Reseptin poisto
```
DELETE FROM resepti WHERE id = ?
DELETE FROM resepti_raaka_aine WHERE resepti_id = ?
```

Rekisteröityminen
```
SELECT COUNT(*) as maara FROM kayttaja WHERE sahkopostiosoite = ?
INSERT INTO kayttaja (sahkopostiosoite, salasana, etunimi, sukunimi) VALUES (?, ?, ?, ?) /* Salasana tallennetaan ei-selkokielisessä muodossa */
```

Kirjautuminen
```
SELECT salasana FROM kayttaja WHERE sahkopostiosoite = ? LIMIT 1 /* Salasanaa käsitellään ei-selkokielisessä muodossa */
```

Reseptin päivittäminen (tulossa)

## Create-kyselyt
Valmistusaika-taulu
```
CREATE TABLE valmistusaika (
        id INTEGER NOT NULL,
        tunti INTEGER NOT NULL,
        minuutti INTEGER NOT NULL,
        PRIMARY KEY (id)
);
```

Käyttäjä-taulu
```
CREATE TABLE kayttaja (
        id INTEGER NOT NULL,
        kayttajatunnus VARCHAR(50),
        salasana VARCHAR(50) NOT NULL,
        etunimi VARCHAR(50) NOT NULL,
        sukunimi VARCHAR(50) NOT NULL,
        sahkopostiosoite VARCHAR(100) NOT NULL,
        rekisteroitynyt DATETIME,
        muokattu DATETIME,
        PRIMARY KEY (id)
);
```

Määrä-yksikkö-taulu
```
CREATE TABLE maara_yksikko (
        id INTEGER NOT NULL,
        nimi VARCHAR(20) NOT NULL,
        ryhma_nro INTEGER NOT NULL,
        PRIMARY KEY (id)
);
```

Resepti-taulu
```
CREATE TABLE resepti (
        id INTEGER NOT NULL,
        nimi VARCHAR(255) NOT NULL,
        valmistusaika_id INTEGER,
        valmistusohje VARCHAR NOT NULL,
        kuvaus VARCHAR(255) NOT NULL,
        luotu DATETIME,
        kayttaja_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(valmistusaika_id) REFERENCES valmistusaika (id),
        FOREIGN KEY(kayttaja_id) REFERENCES kayttaja (id)
);
```

Raaka-aine-taulu
```
CREATE TABLE raaka_aine (
        id INTEGER NOT NULL,
        nimi VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
);
```

Resepti-raaka-aine-taulu (sekä liitos- että normaalitaulu lisätiedoilla (määrä) eli voisiko sanoa "hybriditaulu"?)
```
CREATE TABLE resepti_raaka_aine (
        id INTEGER NOT NULL,
        resepti_id INTEGER,
        raaka_aine_id INTEGER,
        maara NUMERIC(3) NOT NULL,
        maara_yksikko_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(resepti_id) REFERENCES resepti (id),
        FOREIGN KEY(raaka_aine_id) REFERENCES raaka_aine (id),
        FOREIGN KEY(maara_yksikko_id) REFERENCES maara_yksikko (id)
);
```
