# Tietokantakyselyjä
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
