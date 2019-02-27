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

... päivitetään myöhemmin.
