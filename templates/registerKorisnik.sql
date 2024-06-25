INSERT INTO korisnik (ime, prezime, username, password, id_ovlasti) VALUES
(%s, %s, %s, UNHEX(SHA2(%s, 256)), %s)
