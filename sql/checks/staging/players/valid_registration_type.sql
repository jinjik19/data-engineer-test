SELECT count() AS bad_rows
FROM staging.players
WHERE registration_type NOT IN ('standard', 'premium', 'vip');