CREATE TABLE IF NOT EXISTS raw.players 
(
    id UInt32,
    registration_date Date,
    registration_type LowCardinality(String),
    LowCardinality LowCardinality(String),
    loaded_at DateTime('UTC') DEFAULT now()
)
ENGINE = MergeTree
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.providers_map
(
    id UInt32,
    provider_name String,
    loaded_at DateTime('UTC') DEFAULT now()
)
ENGINE MergeTree
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.games_map
(
    id UInt32,
    game_name String,
    provider_id UInt32,
    loaded_at DateTime('UTC') DEFAULT now()
)
ENGINE = MergeTree
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.currency_rates
(
    date Date,
    currency LowCardinality(String),
    rate_to_usd Decimal(10, 4),
    loaded_at DateTime('UTC') DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (currency, date);

CREATE TABLE IF NOT EXISTS raw.deposits
(
    id UInt32,
    player_id UInt32,
    deposit_date Date,
    provider_id UInt32,
    amount Decimal(10, 2),
    currency LowCardinality(String),
    loaded_at DateTime('UTC') DEFAULT now()
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(deposit_date)
ORDER BY (deposit_date, player_id, id);

CREATE TABLE IF NOT EXISTS raw.withdrawals
(
    id UInt32,
    player_id UInt32,
    withdrawal_date Date,
    provider_id UInt32,
    amount Decimal(10, 2),
    currency LowCardinality(String),
    loaded_at DateTime('UTC') DEFAULT now()
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(withdrawal_date)
ORDER BY (withdrawal_date, player_id, id);

CREATE TABLE IF NOT EXISTS raw.games
(
    id UInt32,
    player_id UInt32,
    game_date Date,
    amount Decimal(10, 2),
    currency LowCardinality(String),
    provider_id UInt32,
    game_id UInt32,
    loaded_at DateTime('UTC') DEFAULT now()
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(game_date)
ORDER BY (game_date, player_id, game_id, id);