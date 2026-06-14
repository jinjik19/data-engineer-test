SELECT count() AS bad_rows
FROM staging.currency_rates
WHERE rate_to_usd <= 0;