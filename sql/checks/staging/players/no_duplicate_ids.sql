SELECT count() - uniqExact(id) AS bad_rows
FROM staging.players;