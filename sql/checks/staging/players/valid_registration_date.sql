SELECT count() AS bad_rows
FROM staging.players
WHERE registration_date < toDate('2000-01-01')
   OR registration_date > today();