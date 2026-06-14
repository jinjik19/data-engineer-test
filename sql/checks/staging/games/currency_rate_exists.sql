SELECT count() AS bad_rows
FROM staging.games g
WHERE NOT EXISTS (
    SELECT 1
    FROM staging.currency_rates cr
    WHERE cr.date = g.game_date
      AND cr.currency = g.currency
);