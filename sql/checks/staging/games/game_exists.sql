SELECT count() AS bad_rows
FROM staging.games g
WHERE NOT EXISTS
(
    SELECT 1
    FROM staging.games_map gm
    WHERE gm.id = g.game_id
);