/* Luo taulut uudelleen poistamalla olemassa oleva ja luomalla sitten sama taulu uudelleen */

/* Valmistusaika-taulu */
DROP TABLE IF EXISTS Valmistusaika;

CREATE TABLE Valmistusaika (
    id integer NOT NULL,
    tunti integer NOT NULL,
    minuutti integer NOT NULL,
    PRIMARY KEY (id)
);

/* ReseptiValinta-taulu */
DROP TABLE IF EXISTS ReseptiValinta;

CREATE TABLE ReseptiValinta (
    id integer NOT NULL,
    nimi varchar(50) NOT NULL,
    PRIMARY KEY (id)
);

/* Kayttajataso-taulu */
DROP TABLE IF EXISTS Kayttajataso;

CREATE TABLE Kayttajataso (
    id integer NOT NULL,
    nimi varchar(50) NOT NULL,
    PRIMARY KEY (id)
);

/* Resepti-taulu */
DROP TABLE IF EXISTS Resepti;

CREATE TABLE Resepti (
    id integer NOT NULL,
    nimi varchar(255) NOT NULL,
    valmistusaika_id integer NOT NULL,
    valmistusohje text NOT NULL,
    kuvaus varchar(255) NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (valmistusaika_id) REFERENCES Valmistusaika(id)
);

/* Kayttaja-taulu */
DROP TABLE IF EXISTS Kayttaja;

CREATE TABLE Kayttaja (
    id integer NOT NULL,
    kayttajataso_id integer NOT NULL,
    kayttajatunnus varchar(50) NOT NULL,
    salasana_hash varchar(50) NOT NULL,
    sahkopostiosoite varchar(50) NOT NULL,
    etunimi varchar(50) NULL,
    sukunimi varchar(50) NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (kayttajataso_id) REFERENCES Kayttajataso(id)
);

/* Reseptiryhma-taulu */
DROP TABLE IF EXISTS Reseptiryhma;

CREATE TABLE Reseptiryhma (
    id integer NOT NULL,
    yla_ryhma_id integer NOT NULL,
    nimi varchar(100) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (yla_ryhma_id) REFERENCES Reseptiryhma(id)
);

/* RaakaAine-taulu */
DROP TABLE IF EXISTS RaakaAine;

CREATE TABLE RaakaAine (
    id integer NOT NULL,
    nimi varchar(100) NOT NULL,
    maara double NOT NULL,
    maara_yksikko_id integer NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (maara_yksikko_id) REFERENCES MaaraYksikko(id)
);

/* MaaraYksikko-taulu */
DROP TABLE IF EXISTS MaaraYksikko;

CREATE TABLE MaaraYksikko (
    id integer NOT NULL,
    nimi varchar(20) NOT NULL,
    PRIMARY KEY (id)
);

/* ReseptiRaakaAine-taulu */
DROP TABLE IF EXISTS ReseptiRaakaAine;

CREATE TABLE ReseptiRaakaAine (
    resepti_id integer NOT NULL,
    raaka_aine_id integer NOT NULL,
    FOREIGN KEY (resepti_id) REFERENCES Resepti(id),
    FOREIGN KEY (raaka_aine_id) REFERENCES RaakaAine(id)
);

/* ReseptiKayttaja-taulu */
DROP TABLE IF EXISTS ReseptiKayttaja;

CREATE TABLE ReseptiKayttaja (
    resepti_id integer NOT NULL,
    kayttaja_id integer NOT NULL,
    FOREIGN KEY (resepti_id) REFERENCES Resepti(id),
    FOREIGN KEY (kayttaja_id) REFERENCES Kayttaja(id)
);

/* ReseptiReseptiryhma-taulu */
DROP TABLE IF EXISTS ReseptiReseptiryhma;

CREATE TABLE ReseptiReseptiryhma (
    resepti_id integer NOT NULL,
    reseptiryhma_id integer NOT NULL,
    FOREIGN KEY (resepti_id) REFERENCES Resepti(id),
    FOREIGN KEY (reseptiryhma_id) REFERENCES Reseptiryhma(id)
);

/* ReseptiReseptiValinta-taulu */
DROP TABLE IF EXISTS ReseptiReseptiValinta;

CREATE TABLE ReseptiReseptiValinta (
    resepti_id integer NOT NULL,
    resepti_valinta_id integer NOT NULL,
    arvo integer NOT NULL,
    FOREIGN KEY (resepti_id) REFERENCES Resepti(id),
    FOREIGN KEY (resepti_valinta_id) REFERENCES ReseptiValinta(id)
);