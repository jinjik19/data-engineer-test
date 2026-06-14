SELECT count() AS bad_rows
FROM staging.games_map
WHERE game_name = '';