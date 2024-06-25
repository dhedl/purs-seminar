INSERT INTO aktivnosti (id_korisnika, id_ormarica, akcija)
SELECT k.id, NULL, CONCAT('Login korisnika ', k.username) AS akcija
FROM korisnik k
WHERE k.id = %s;
