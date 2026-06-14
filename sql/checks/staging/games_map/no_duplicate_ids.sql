SELECT count() - uniqExact(id) AS bad_rows
FROM staging.games_map;