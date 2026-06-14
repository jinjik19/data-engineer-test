SELECT count() AS bad_rows
FROM staging.currency_rates
WHERE currency = '';