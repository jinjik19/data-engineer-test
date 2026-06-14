SELECT count() AS bad_rows
FROM staging.deposits d
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.currency_rates cr
    WHERE cr.date = d.deposit_date
      AND cr.currency = d.currency
);