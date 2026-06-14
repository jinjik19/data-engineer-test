SELECT count() AS bad_rows
FROM staging.currency_rates
WHERE date < toDate('2000-01-01')
   OR date > today();