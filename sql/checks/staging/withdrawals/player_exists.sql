SELECT count() AS bad_rows
FROM staging.withdrawals AS w
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.players AS p
    WHERE p.id = w.player_id
);