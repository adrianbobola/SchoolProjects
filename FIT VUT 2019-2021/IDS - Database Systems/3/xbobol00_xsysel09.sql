-- IDS 2020/2021 | Autor: xbobol00, xsysel09

DROP TABLE Aliance CASCADE CONSTRAINTS;
DROP TABLE Kapitan CASCADE CONSTRAINTS;
DROP TABLE Lod CASCADE CONSTRAINTS;
DROP TABLE Pirat CASCADE CONSTRAINTS;
DROP TABLE Posadka CASCADE CONSTRAINTS;
DROP TABLE Pristav CASCADE CONSTRAINTS;
DROP TABLE Radovy_pirat CASCADE CONSTRAINTS;
DROP TABLE Bitva CASCADE CONSTRAINTS;
DROP TABLE Pirat_veli_lod CASCADE CONSTRAINTS;
DROP TABLE Lod_bojovala_v_bitva CASCADE CONSTRAINTS;

CREATE TABLE Pirat
(
    id              INT GENERATED AS IDENTITY PRIMARY KEY,
    jmeno           VARCHAR(80) CHECK (REGEXP_LIKE(jmeno, '([[:graph:]]{2,}?)+')), -- min 2 znaky za sebou
    prezdivka       VARCHAR(80)  NOT NULL,
    vek             INT          NOT NULL CHECK ( vek > 0 ),
    barva_vousu     VARCHAR(80)  NOT NULL,
    cas_sluzby      DATE         ,
    charakteristiky VARCHAR(255) NOT NULL,
    plavi_se_na     INT
);

CREATE TABLE Radovy_pirat
(
    id         INT PRIMARY KEY,
    pozice     VARCHAR(80),
    je_soucast VARCHAR(20)
);

CREATE TABLE Kapitan
(
    id INT PRIMARY KEY
);

CREATE TABLE Posadka
(
    jmeno         VARCHAR(20) PRIMARY KEY CHECK (REGEXP_LIKE(jmeno, '([[:graph:]]{2,}?)+')), -- min 2 znaky za sebou
    jolly_roger   VARCHAR(255) NOT NULL,
    tvori_alianci VARCHAR(80),
    vlastni       INT          NOT NUll
);

CREATE TABLE Lod
(
    id       INT GENERATED AS IDENTITY NOT NULL PRIMARY KEY,
    typ      VARCHAR(80)               NOT NULL,
    kapacita INT                       NOT NULL CHECK ( kapacita > 0 ),
    patri    INT,
    kotvi    INT

);

CREATE TABLE Pirat_veli_lod
(
    id       INT GENERATED AS IDENTITY PRIMARY KEY,
    id_pirat INT NOT NULL,
    id_lod   INT NOT NULL,
    CONSTRAINT pirat_veli_fk FOREIGN KEY (id_pirat) REFERENCES Pirat (id) ON DELETE CASCADE,
    CONSTRAINT lod_veli_fk FOREIGN KEY (id_lod) REFERENCES Lod (id) ON DELETE CASCADE
);

CREATE TABLE Pristav
(
    id            INT GENERATED AS IDENTITY PRIMARY KEY,
    nazev_ostrova VARCHAR(80) NOT NULL CHECK (REGEXP_LIKE(nazev_ostrova, '([[:graph:]]{2,}?)+')), -- min 2 znaky za sebou
    kapacita      INT         NOT NULL CHECK ( kapacita > 0 ),
    je_teritorium VARCHAR(20)
);

CREATE TABLE Aliance
(
    nazev   VARCHAR(80) PRIMARY KEY CHECK (REGEXP_LIKE(nazev, '([[:graph:]]{2,}?)+')), -- min 2 znaky za sebou
    sidli_v INT
);

CREATE TABLE Bitva
(
    id         INT GENERATED AS IDENTITY PRIMARY KEY,
    datum      DATE NOT NULL,
    ztraty     INT  NOT NULL CHECK ( ztraty >= 0 ),
    probehla_v INT
);

CREATE TABLE Lod_bojovala_v_bitva
(
    id       INT GENERATED as IDENTITY PRIMARY KEY,
    id_lod   INT NOT NULL,
    id_bitva INT NOT NULL,
    CONSTRAINT lod_bojovala_fk FOREIGN KEY (id_lod) REFERENCES Lod (id) ON DELETE CASCADE,
    CONSTRAINT bitva_bojovala_fk FOREIGN KEY (id_bitva) REFERENCES Bitva (id) ON DELETE CASCADE
);

ALTER TABLE Lod
    ADD CONSTRAINT patri_fk FOREIGN KEY (patri) REFERENCES Kapitan (id) ON DELETE SET NULL;
ALTER TABLE Lod
    ADD CONSTRAINT kotvi_fk FOREIGN KEY (kotvi) REFERENCES Pristav (id) ON DELETE SET NULL;
ALTER TABLE Pirat
    ADD CONSTRAINT plavi_se_na_fk FOREIGN KEY (plavi_se_na) REFERENCES Lod (id) ON DELETE SET NULL;
ALTER TABLE Kapitan
    ADD CONSTRAINT kapitan_fk FOREIGN KEY (id) REFERENCES Pirat (id) ON DELETE CASCADE;
ALTER TABLE Posadka
    ADD CONSTRAINT tvori_alianci_fk FOREIGN KEY (tvori_alianci) REFERENCES Aliance (nazev) ON DELETE SET NULL;
ALTER TABLE Posadka
    ADD CONSTRAINT vlastni_fk FOREIGN KEY (vlastni) REFERENCES Kapitan (id) ON DELETE CASCADE;
ALTER TABLE Radovy_pirat
    ADD CONSTRAINT pirat_fk FOREIGN KEY (id) REFERENCES Pirat (id) ON DELETE CASCADE;
ALTER TABLE Radovy_pirat
    ADD CONSTRAINT je_soucast_fk FOREIGN KEY (je_soucast) REFERENCES Posadka (jmeno) ON DELETE SET NULL;
ALTER TABLE Pristav
    ADD CONSTRAINT je_teritorium_fk FOREIGN KEY (je_teritorium) REFERENCES Posadka (jmeno) ON DELETE SET NULL;
ALTER TABLE Aliance
    ADD CONSTRAINT sidli_v_fk FOREIGN KEY (sidli_v) REFERENCES Pristav (id) ON DELETE SET NULL;
ALTER TABLE Bitva
    ADD CONSTRAINT probleha_v_fk FOREIGN KEY (probehla_v) REFERENCES Pristav (id) ON DELETE SET NULL;

------------------------ Insert Values ----------------------
--pirat
INSERT INTO Pirat (jmeno, prezdivka, vek, barva_vousu, cas_sluzby, charakteristiky, plavi_se_na)
VALUES (NULL, 'Pirát z Karibiku', 45, 'Hneda, cerna', DATE '1999-8-1', 'Podezřele často se propadává podlahou.', NULL);

INSERT INTO Pirat (jmeno, prezdivka, vek, barva_vousu, cas_sluzby, charakteristiky, plavi_se_na)
VALUES ('John Dohn', 'Šavlozubý', 69, 'stříbrná', DATE '1975-1-20', 'Kulhá, nedoslýchá, páska přes oko.', NULL);

INSERT INTO Pirat (jmeno, prezdivka, vek, barva_vousu, cas_sluzby, charakteristiky, plavi_se_na)
VALUES (NULL, 'Červený šátek', 1, 'blond', DATE '2000-1-1', 'popáleniny na levé ruce', NULL);

INSERT INTO Pirat (jmeno, prezdivka, vek, barva_vousu, cas_sluzby, charakteristiky, plavi_se_na)
VALUES (NULL, 'Černá skvrna', 999, 'Černá', NULL, 'Je naprosto normální.', NULL);
-- radovy pirat
INSERT INTO Radovy_pirat (id, pozice, je_soucast)
VALUES ((SELECT id FROM Pirat WHERE prezdivka = 'Pirát z Karibiku'), NULL, NULL);
INSERT INTO Radovy_pirat (id, pozice, je_soucast)
VALUES ((SELECT id FROM Pirat WHERE jmeno = 'John Dohn'), NULL, NULL);
--kapitan
INSERT INTO Kapitan (id)
VALUES ((SELECT id FROM Pirat WHERE prezdivka = 'Červený šátek'));
-- lod
INSERT INTO Lod (typ, kapacita, patri, kotvi)
VALUES ('Briga', '6', (SELECT id FROM Pirat WHERE prezdivka = 'Červený šátek'), NULL);
INSERT INTO Lod (typ, kapacita, patri, kotvi)
VALUES ('Člun', '2', (SELECT id FROM Pirat WHERE prezdivka = 'Červený šátek'), NULL);
-- pridat vztah: pirat se plavi na lod
UPDATE Pirat
SET plavi_se_na = (SELECT id from Lod WHERE patri IN (SELECT id from Pirat WHERE prezdivka = 'Červený šátek') and typ = 'Briga')
WHERE prezdivka = 'Pirát z Karibiku'
   OR prezdivka = 'Šavlozubý'
   or prezdivka = 'Červený šátek';
-- posadka
INSERT INTO Posadka (jmeno, jolly_roger, tvori_alianci, vlastni)
VALUES ('Johnnyho banda', 'Černá lebka na černém pozadí', NULL,
        (SELECT id FROM Pirat WHERE prezdivka = 'Červený šátek'));
-- pristav
INSERT INTO Pristav (nazev_ostrova, kapacita, je_teritorium)
VALUES ('Celjón', 50, (SELECT jmeno FROM Posadka WHERE jmeno = 'Johnnyho banda'));
INSERT INTO Pristav (nazev_ostrova, kapacita, je_teritorium)
VALUES ('Jáva', 10, NULL);
-- aliance
INSERT INTO Aliance (nazev, sidli_v)
VALUES ('Východní obchodní společnost', (SELECT id FROM Pristav WHERE nazev_ostrova = 'Celjón'));
-- bitva
INSERT INTO Bitva (datum, ztraty, probehla_v)
VALUES (DATE '2015-08-03', 40, (SELECT id FROM Pristav WHERE nazev_ostrova = 'Celjón'));
-- radovy pirat - doplneni
UPDATE Radovy_pirat
SET pozice     = 'Kormidelník',
    je_soucast = 'Johnnyho banda'
WHERE id in (SELECT id FROM Pirat where prezdivka = 'Pirát z Karibiku');
-- radovy pirat - doplneni
UPDATE Radovy_pirat
SET pozice     = 'Tesar',
    je_soucast = 'Johnnyho banda'
WHERE id in (SELECT id FROM Pirat where prezdivka = 'Šavlozubý');
-- lod - doplneni udaju
UPDATE Lod
SET kotvi = (SELECT id FROM Pristav where nazev_ostrova = 'Celjón')
WHERE patri in (SELECT id FROM Pirat where prezdivka = 'Červený šátek');
-- posadka - doplneni
UPDATE Posadka
SET tvori_alianci = 'Východní obchodní společnost'
WHERE vlastni in (SELECT id FROM Pirat where prezdivka = 'Červený šátek');
-- doplneni vztahu
INSERT INTO Pirat_veli_lod (id_pirat, id_lod)
VALUES ((SELECT id FROM Pirat where prezdivka = 'Červený šátek'),
        (SELECT id FROM Lod where patri in ((SELECT id FROM Pirat where prezdivka = 'Červený šátek')) and typ = 'Briga'));
-- doplneni vztahu
INSERT INTO Lod_bojovala_v_bitva (id_lod, id_bitva)
VALUES ((SELECT id FROM Lod where patri in ((SELECT id FROM Pirat where prezdivka = 'Červený šátek')) and typ = 'Briga'),
        (SELECT id FROM Bitva WHERE datum = DATE '2015-08-03'));

/*
-- VYPIS TABULEK:
SELECT *
FROM Pirat;
SELECT *
FROM Radovy_pirat;
SELECT *
FROM Kapitan;
SELECT *
FROM Lod;
SELECT *
FROM Posadka;
SELECT *
FROM Aliance;
SELECT *
FROM Pristav;
SELECT *
FROM Bitva;
SELECT *
FROM Pirat_veli_lod;
SELECT *
FROM Lod_bojovala_v_bitva;
*/

----------------------Třetí projekt----------------------

--spojení dvou tabulek
--Kteří piráti jsou kapitány?
SELECT *
FROM Pirat
NATURAL JOIN Kapitan;

--spojení dvou tabulek
--Kolik volných míst mají jednotlivé lodě?
SELECT Lod.id                                Lod_id,
       Lod.kapacita - COUNT(UNIQUE Pirat.id) volnych_mist
FROM Lod
         LEFT JOIN Pirat ON plavi_se_na = Lod.id
GROUP BY Lod.id, Lod.kapacita;

--spojení tří tabulek
--Ve kterém přístavu kotví kteří piráti?
SELECT
    Pirat.id id_pirata,
    Pirat.prezdivka,
    Pristav.id id_pristavu,
    Pristav.nazev_ostrova
FROM Pirat
    LEFT JOIN Lod on Pirat.plavi_se_na = Lod.id
    LEFT JOIN Pristav on Lod.kotvi = Pristav.id;


--klauzule GROUP BY a agregační funkce
--Kolik je pirátů mladších 30 let?
SELECT COUNT(DISTINCT Pirat.id) pocet
FROM Pirat
WHERE Pirat.vek < 30
GROUP BY Pirat.vek;

--klauzule GROUP BY a agregační funkce
--Kolik lodí vlastní jednotlivé posádky?
SELECT Posadka.jmeno, COUNT(DISTINCT Lod.id) pocet_lodi
FROM POSADKA
         JOIN Lod on Posadka.vlastni = Lod.patri
GROUP BY Posadka.jmeno
ORDER BY pocet_lodi;

--predikát EXISTS
--Na kterých lodích se nikdo neplaví?
SELECT *
FROM Lod
WHERE NOT EXISTS(
    SELECT * FROM Pirat
    WHERE plavi_se_na = Lod.id
    );

--predikát IN s vnořeným SELECTem
--Které lodě patří pirátovy s přezdívkou Červený šátek?
SELECT *
FROM Lod
WHERE patri IN (
    SELECT id
    FROM Pirat
    WHERE prezdivka = 'Červený šátek'
    );