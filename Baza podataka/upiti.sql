-- upiti

SELECT * FROM ormarici;	

SELECT * FROM aktivnosti;

SELECT * FROM korisnik;

SELECT id FROM ormarici WHERE zauzet = 0 ORDER BY id LIMIT 1;

SELECT * FROM korisnik_ormaric;

SELECT id FROM ormarici WHERE zauzet = 0 ORDER BY id LIMIT 1;