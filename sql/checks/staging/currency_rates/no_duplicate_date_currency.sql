SELECT count() - uniqExact(tuple(date, currency)) AS bad_rows
FROM staging.currency_rates;