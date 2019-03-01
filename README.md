# Recipe book
A simple recipe book with Python backend. All comments and commits will be written in Finnish.

Tämä projekti on osa Tietokantasovellus-kurssin suoritusta, minkä vuoksi kommentit (koodissa) ja commitit kirjoitetaan suomeksi.

"Reseptikirja" on suunniteltu yksinkertaiseksi palveluksi, jossa käyttäjät voivat lisätä omia reseptejään ja jakaa niitä muiden kanssa. Palvelun käyttö ei vaadi rekisteröitymistä mikäli haluaa vain selata eri reseptejä mutta lisäys ym. vaativat rekisteröitymisen. Ulkoasuna käytetään Bootstrap (https://getbootstrap.com) nimistä pakettia ja kuvakkeina Feathericons-kuvakepaketista (https://feathericons.com, lisenssi: MIT) saatavilla olevia kuvakkeita SVG-muodossa. Sovellus suunnitellaan sekä tietokone- että mobiilikäyttäjille.

Sovellus on nähtävillä vain omalla palvelimellani (ei Herokussa! Koska tämän projektin osalta Herokussa ei pysty suorittamaan edes perus SELECT COUNT(\*) as maara FROM taulu -kyselyä PostgreSQL-tietokannassa) osoitteessa: http://86.60.242.10:5060.

Dokumentaatiossa on saatavilla [asennus](https://github.com/Vilthsu/recipebook/blob/master/documentation/asennus.md), [(loppu)käyttäjän käyttöohjeet](https://github.com/Vilthsu/recipebook/blob/master/documentation/kayttajan-ohjeet.md), [toteutuneet relaatiokaaviot](https://github.com/Vilthsu/recipebook/blob/master/documentation/relaatiokaaviot.md), [user storyt](https://github.com/Vilthsu/recipebook/blob/master/documentation/user-storyt.md), käyttöehdot (tulossa myöhemmin), [tietokantakyselyjä](https://github.com/Vilthsu/recipebook/blob/master/documentation/tietokantakyselyja.md), [tavoitteet](https://github.com/Vilthsu/recipebook/blob/master/documentation/tavoitteet.md) (sisältää tiedot puuttuvista ja suunnitteilla olevista ominaisuuksista) ja [tietoja yksityisyydestä](https://github.com/Vilthsu/recipebook/blob/master/documentation/yksityisyys.md), joka sisältää muun muassa tietojen käytön ja käsittelyn. Nämä tiedostot löytyvät erillisinä md-tiedostoina documentation-hakemistosta.

TODO-lista ominaisuuksista ym. on löydettävissä repositoryn issues -osiosta.

~Sovellus on nähtävillä Herokussa osoitteessa: https://frozen-ocean-30894.herokuapp.com/ (repositoryn "recipebook" nimi ei ollut vapaana Herokussa)~

## Testitunnukset
| Sähköpostiosoite | Salasana |
|------------------|----------|
| test@localhost   | test1234 |

(Voit myös luoda omat tunnukset rekisteröitymissivun avulla)

## Branchit
Kaikki harjoitustyöhön liittyvät commitit julkaistaan master ja deadline(2-4) (tms.) -brancheilla (useimmiten harjoitustyöhön liittyvät branchit yhdistetään master-branchiin jossain kohtaa). Repoon voi tulla jossain kohtaa muita brancheja (joiden sisältö voi olla myös englanniksi), jotka eivät liity harjoitustyöhön kuten api-rajapinta, joka mahdollistaa palvelun liittämisen muihin sovelluksiin. Master-branchi on suojattu ja pull requestit vaativat repositoryn omistajan hyväksynnän.
