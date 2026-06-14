SELECT count() AS bad_rows
FROM staging.withdrawals
WHERE withdrawal_date < toDate('2000-01-01')
   OR withdrawal_date > today();