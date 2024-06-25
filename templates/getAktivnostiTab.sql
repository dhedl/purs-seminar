SELECT a.id, k.ime, k.prezime, a.timestamp, a.akcija 
FROM aktivnosti a
JOIN korisnik k ON a.id_korisnika = k.id
ORDER BY a.id DESC;
