WITH lastest_load_batch AS (
    SELECT
        data_month,
        argMax(load_id, loaded_at) AS latest_load_id
    FROM raw.load_batches
    WHERE entity = 'games'
      AND status = 'success'
    GROUP BY data_month
)
INSERT INTO staging.games
SELECT
    g.id,
    g.player_id,
    g.game_date,
    g.amount,
    g.currency,
    g.provider_id,
    g.game_id,
    g.loaded_at AS updated_at
FROM raw.games g
INNER JOIN lastest_load_batch lb
    ON toStartOfMonth(g.game_date) = lb.data_month
   AND g.load_id = lb.latest_load_id
ORDER BY g.loaded_at DESC
LIMIT 1 BY g.id;