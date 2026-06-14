CREATE TABLE IF NOT EXISTS mart.monthly_summary
(
    month Date,
    country LowCardinality(String),
    deposit_amount_usd Decimal(12, 2),
    withdrawal_amount_usd Decimal(12, 2),
    bet_amount_usd Decimal(12, 2)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(month)
ORDER BY (month, country);