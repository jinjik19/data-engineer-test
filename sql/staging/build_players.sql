INSERT INTO staging.players
SELECT
    id,
    registration_date,
    registration_type,
    country,
    loaded_at AS updated_at
FROM raw.players
WHERE load_id = (
    SELECT argMax(load_id, loaded_at) AS latest_load_id
    FROM raw.load_batches
    WHERE entity = 'players'
      AND data_month = toDate('1970-01-01')
      AND status = 'success'
)
ORDER BY loaded_at DESC
LIMIT 1 BY id;