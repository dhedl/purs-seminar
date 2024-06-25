INSERT INTO ormarici (id, zauzet)
SELECT COALESCE(MIN(id + 1), 1), 0
FROM ormarici
WHERE (id + 1) NOT IN (SELECT id FROM ormarici);