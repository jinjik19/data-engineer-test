INSERT INTO staging.games_map
SELECT
    id,
    game_name,
    provider_id,
    loaded_at AS updated_at
FROM raw.games_map
WHERE load_id = (
    SELECT argMax(load_id, loaded_at)
    FROM raw.load_batches
    WHERE entity = 'games_map'
      AND data_month = toDate('1970-01-01')
      AND status = 'success'
)
ORDER BY loaded_at DESC
LIMIT 1 BY id;