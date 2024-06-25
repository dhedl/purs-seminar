UPDATE ormarici
SET zauzet = 1 - zauzet
WHERE id = %s;