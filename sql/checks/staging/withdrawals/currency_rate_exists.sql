SELECT count() AS bad_rows
FROM staging.withdrawals w
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.currency_rates cr
    WHERE cr.date = w.withdrawal_date
      AND cr.currency = w.currency
);