SELECT count() AS bad_rows
FROM staging.deposits
WHERE amount <= 0;