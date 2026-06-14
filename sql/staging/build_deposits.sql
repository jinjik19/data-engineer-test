WITH lastest_load_batch AS (
    SELECT
        data_month,
        argMax(load_id, loaded_at) AS latest_load_id
    FROM raw.load_batches
    WHERE entity = 'deposits'
      AND status = 'success'
    GROUP BY data_month
)
INSERT INTO staging.deposits
SELECT
    d.id,
    d.player_id,
    d.deposit_date,
    d.provider_id,
    d.amount,
    d.currency,
    d.loaded_at AS updated_at
FROM raw.deposits d
INNER JOIN lastest_load_batch lb
    ON toStartOfMonth(d.deposit_date) = lb.data_month 
    AND d.load_id = lb.latest_load_id
ORDER BY d.loaded_at DESC
LIMIT 1 BY d.id;