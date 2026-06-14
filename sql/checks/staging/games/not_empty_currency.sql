SELECT count() AS bad_rows
FROM staging.games
WHERE currency = '';