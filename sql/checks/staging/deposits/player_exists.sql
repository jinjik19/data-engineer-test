SELECT count() AS bad_rows
FROM staging.deposits d
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.players p
    WHERE p.id = d.player_id
);