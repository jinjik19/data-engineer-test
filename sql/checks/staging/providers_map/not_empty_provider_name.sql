SELECT count() AS bad_rows
FROM staging.providers_map
WHERE provider_name = '';