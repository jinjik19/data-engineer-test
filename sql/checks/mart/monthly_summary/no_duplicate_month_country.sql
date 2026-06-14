SELECT count() - uniqExact(tuple(month, country)) AS bad_rows
FROM mart.monthly_summary;