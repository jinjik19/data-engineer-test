CREATE TABLE IF NOT EXISTS raw.players
(
    id UInt32,
    registration_date Date,
    registration_type LowCardinality(String),
    country LowCardinality(String),

    source_file String,
    load_id UUID,
    loaded_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree(loaded_at)
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.providers_map
(
    id UInt32,
    provider_name String,

    source_file String,
    load_id UUID,
    loaded_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree(loaded_at)
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.games_map
(
    id UInt32,
    game_name String,
    provider_id UInt32,

    source_file String,
    load_id UUID,
    loaded_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree(loaded_at)
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.games_map
(
    id UInt32,
    game_name String,
    provider_id UInt32,

    source_file String,
    load_id UUID,
    loaded_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree(loaded_at)
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.deposits
(
    id UInt32,
    player_id UInt32,
    deposit_date Date,
    provider_id UInt32,
    amount Decimal(10, 2),
    currency LowCardinality(String),

    source_file String,
    load_id UUID,
    loaded_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree(loaded_at)
PARTITION BY toYYYYMM(deposit_date)
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.withdrawals
(
    id UInt32,
    player_id UInt32,
    withdrawal_date Date,
    provider_id UInt32,
    amount Decimal(10, 2),
    currency LowCardinality(String),

    source_file String,
    load_id UUID,
    loaded_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree(loaded_at)
PARTITION BY toYYYYMM(withdrawal_date)
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.games
(
    id UInt32,
    player_id UInt32,
    game_date Date,
    amount Decimal(10, 2),
    currency LowCardinality(String),
    provider_id UInt32,
    game_id UInt32,

    source_file String,
    load_id UUID,
    loaded_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree(loaded_at)
PARTITION BY toYYYYMM(game_date)
ORDER BY id;

CREATE TABLE IF NOT EXISTS raw.load_batches
(
    entity LowCardinality(String),
    data_month Date,
    load_id UUID,
    source_file String,
    loaded_at DateTime64(3, 'UTC'),
    status LowCardinality(String)
)
ENGINE = ReplacingMergeTree(loaded_at)
ORDER BY (entity, data_month, load_id);