-- Izrada i odabir baze
DROP DATABASE IF EXISTS purs;
CREATE DATABASE IF NOT EXISTS purs;
USE purs;

DROP USER IF EXISTS app;
CREATE USER app@'%' IDENTIFIED BY '1234';
GRANT SELECT, INSERT, UPDATE, DELETE ON purs.* TO app@'%';

-- Izrada tablice ovlasti
CREATE TABLE ovlasti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    naziv VARCHAR(100)
);

-- Unos podataka u tablicu ovlasti
INSERT INTO ovlasti (naziv)
VALUES
    ('Administrator'),
    ('Korisnik');
    
-- Izrada tablice korisnik
CREATE TABLE korisnik (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ime CHAR(50),
    prezime CHAR(50),
    username VARCHAR(50),
    password VARBINARY(50),
    id_ovlasti INT,
    FOREIGN KEY (id_ovlasti) REFERENCES ovlasti(id) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Unos podataka u tablicu korisnik
INSERT INTO korisnik (ime, prezime, username, password, id_ovlasti)
VALUES
    ('Haniel', 'Dedl', 'hdedl', UNHEX(SHA2('1234', 256)), 1),
    ('Parko', 'Mavlek', 'pmavlek', UNHEX(SHA2('abcd', 256)), 1),
    ('Danko', 'Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), 2),
    ('Katija', 'Kolar', 'kkolar', UNHEX(SHA2('12ab', 256)), 2);

-- Izrada tablice za ormariće
CREATE TABLE ormarici (
    id INT AUTO_INCREMENT PRIMARY KEY,
    zauzet INT DEFAULT 0
);

-- Unos podataka u tablicu ormarići
INSERT INTO ormarici (id, zauzet)
VALUES
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (7, 1);
    
-- Izrada tablice korisnik_ormaric 
CREATE TABLE korisnik_ormaric (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_korisnika INT,
    id_ormarica INT,
    sifra_ormarica VARCHAR(50),	
    datum_iznajmljivanja DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_korisnika) REFERENCES korisnik(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_ormarica) REFERENCES ormarici(id) ON UPDATE CASCADE ON DELETE CASCADE
);
    
-- Izrada tablice za evidenciju korištenja ormarića
CREATE TABLE aktivnosti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_korisnika INT,
    id_ormarica INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    akcija VARCHAR(50),
    FOREIGN KEY (id_korisnika) REFERENCES korisnik(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_ormarica) REFERENCES ormarici(id) ON UPDATE CASCADE ON DELETE CASCADE
);
    
INSERT INTO aktivnosti (id_korisnika, id_ormarica, akcija)
VALUES
    (1, 1, 'Iznajmljen ormarić'),
    (2, 3, 'Iznajmljen ormarić'),  
    (1, 1, 'Vraćen ormarić'),      
    (3, 5, 'Iznajmljen ormarić');  