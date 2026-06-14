SELECT count() AS bad_rows
FROM staging.games g
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.providers_map pm
    WHERE pm.id = g.provider_id
);