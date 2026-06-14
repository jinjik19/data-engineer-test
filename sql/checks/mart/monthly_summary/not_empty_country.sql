SELECT count() AS bad_rows
FROM mart.monthly_summary
WHERE country = '';