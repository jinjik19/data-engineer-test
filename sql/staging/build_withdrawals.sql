WITH lastest_load_batch AS (
    SELECT
        data_month,
        argMax(load_id, loaded_at) AS latest_load_id
    FROM raw.load_batches
    WHERE entity = 'withdrawals'
      AND status = 'success'
    GROUP BY data_month
)
INSERT INTO staging.withdrawals
SELECT
    w.id,
    w.player_id,
    w.withdrawal_date,
    w.provider_id,
    w.amount,
    w.currency,
    w.loaded_at AS updated_at
FROM raw.withdrawals w
INNER JOIN lastest_load_batch lb
    ON toStartOfMonth(w.withdrawal_date) = lb.data_month
    AND w.load_id = lb.latest_load_id
ORDER BY w.loaded_at DESC
LIMIT 1 BY w.id;