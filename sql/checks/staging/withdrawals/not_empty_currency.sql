SELECT count() AS bad_rows
FROM staging.withdrawals
WHERE currency = '';