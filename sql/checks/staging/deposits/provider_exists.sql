SELECT count() AS bad_rows
FROM staging.deposits d
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.providers_map pm
    WHERE pm.id = d.provider_id
);