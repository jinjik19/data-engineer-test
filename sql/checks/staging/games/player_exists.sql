SELECT count() AS bad_rows
FROM staging.games g
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.players p
    WHERE p.id = g.player_id
);