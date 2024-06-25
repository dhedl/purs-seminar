SELECT 
    k.id AS korisnik_id, 
    k.ime AS ime, 
    k.prezime AS prezime, 
    k.username AS username, 
    o.naziv AS ovlasti, 
    ko.id_ormarica AS broj_ormarica, 
    COUNT(a.id) AS broj_koristenja_usluge
FROM korisnik k
LEFT JOIN ovlasti o ON k.id_ovlasti = o.id
LEFT JOIN korisnik_ormaric ko ON k.id = ko.id_korisnika
LEFT JOIN aktivnosti a ON k.id = a.id_korisnika
GROUP BY k.id, ko.id_ormarica;
