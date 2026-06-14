SELECT if(count() = 0, 1, 0) AS bad_rows
FROM staging.currency_rates
WHERE currency = 'USD';