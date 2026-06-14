SELECT count() AS bad_rows
FROM staging.players
WHERE country = '';