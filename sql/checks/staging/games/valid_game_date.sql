SELECT count() AS bad_rows
FROM staging.games
WHERE game_date < toDate('2000-01-01')
   OR game_date > today();