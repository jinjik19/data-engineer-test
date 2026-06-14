SELECT count() AS bad_rows
FROM mart.monthly_summary
WHERE month < toDate('2000-01-01')
   OR month > today();