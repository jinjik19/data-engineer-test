SELECT count() AS bad_rows
FROM staging.deposits
WHERE deposit_date < toDate('2000-01-01')
   OR deposit_date > today();