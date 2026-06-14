WITH latest_load_id_by_month AS (
    SELECT
        data_month,
        argMax(load_id, loaded_at) AS latest_load_id
    FROM raw.load_batches
    WHERE entity = 'currency_rates'
      AND status = 'success'
    GROUP BY data_month
)
INSERT INTO staging.currency_rates
SELECT
    date,
    currency,
    rate_to_usd,
    loaded_at AS updated_at
FROM raw.currency_rates cr
INNER JOIN latest_load_id_by_month lb
    ON toStartOfMonth(cr.date) = lb.data_month 
    AND cr.load_id = lb.latest_load_id
ORDER BY loaded_at DESC
LIMIT 1 BY date, currency;