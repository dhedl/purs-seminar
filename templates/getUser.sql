SELECT korisnik.id, korisnik.username, ovlasti.naziv AS ovlasti
FROM korisnik
LEFT JOIN ovlasti ON korisnik.id_ovlasti = ovlasti.id
WHERE username = %s AND password = UNHEX(SHA2(%s, 256));
