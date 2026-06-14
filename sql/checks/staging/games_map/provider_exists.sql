SELECT count() AS bad_rows
FROM staging.games_map gm
WHERE NOT EXISTS
(
    SELECT 1
    FROM staging.providers_map pm
    WHERE pm.id = gm.provider_id
);