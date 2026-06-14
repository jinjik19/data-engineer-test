SELECT count() AS bad_rows
FROM staging.withdrawals w
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.providers_map pm
    WHERE pm.id = w.provider_id
);