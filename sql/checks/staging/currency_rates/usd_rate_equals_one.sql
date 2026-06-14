SELECT count() AS bad_rows
FROM staging.currency_rates
WHERE currency = 'USD'
  AND rate_to_usd != 1;