from de_project.entities.staging_table_config import StagingTableConfig


PLAYERS_CONFIG = StagingTableConfig(
    entity_name="players",
    table_name="staging.players",
    build_sql_file="staging/build_players.sql",
    check_sql_files=(
        "checks/staging/players/not_empty.sql",
        "checks/staging/players/no_duplicate_ids.sql",
        "checks/staging/players/valid_registration_type.sql",
        "checks/staging/players/valid_registration_date.sql",
        "checks/staging/players/not_empty_country.sql",
    ),
)

PROVIDERS_MAP_CONFIG = StagingTableConfig(
    entity_name="providers_map",
    table_name="staging.providers_map",
    build_sql_file="staging/build_providers_map.sql",
    check_sql_files=(
        "checks/staging/providers_map/not_empty.sql",
        "checks/staging/providers_map/no_duplicate_ids.sql",
        "checks/staging/providers_map/not_empty_provider_name.sql",
    ),
)

GAMES_MAP_CONFIG = StagingTableConfig(
    entity_name="games_map",
    table_name="staging.games_map",
    build_sql_file="staging/build_games_map.sql",
    check_sql_files=(
        "checks/staging/games_map/not_empty.sql",
        "checks/staging/games_map/no_duplicate_ids.sql",
        "checks/staging/games_map/not_empty_game_name.sql",
        "checks/staging/games_map/provider_exists.sql",
    ),
)

CURRENCY_RATES_CONFIG = StagingTableConfig(
    entity_name="currency_rates",
    table_name="staging.currency_rates",
    build_sql_file="staging/build_currency_rates.sql",
    check_sql_files=(
        "checks/staging/currency_rates/not_empty.sql",
        "checks/staging/currency_rates/no_duplicate_date_currency.sql",
        "checks/staging/currency_rates/valid_rate_to_usd.sql",
        "checks/staging/currency_rates/not_empty_currency.sql",
        "checks/staging/currency_rates/valid_date_range.sql",
        "checks/staging/currency_rates/has_usd_rate.sql",
        "checks/staging/currency_rates/usd_rate_equals_one.sql",
    ),
)

DEPOSITS_CONFIG = StagingTableConfig(
    entity_name="deposits",
    table_name="staging.deposits",
    build_sql_file="staging/build_deposits.sql",
    check_sql_files=(
        "checks/staging/deposits/not_empty.sql",
        "checks/staging/deposits/no_duplicate_ids.sql",
        "checks/staging/deposits/valid_amount.sql",
        "checks/staging/deposits/not_empty_currency.sql",
        "checks/staging/deposits/valid_deposit_date.sql",
        "checks/staging/deposits/player_exists.sql",
        "checks/staging/deposits/provider_exists.sql",
        "checks/staging/deposits/currency_rate_exists.sql",
    ),
)

WITHDRAWALS_CONFIG = StagingTableConfig(
    entity_name="withdrawals",
    table_name="staging.withdrawals",
    build_sql_file="staging/build_withdrawals.sql",
    check_sql_files=(
        "checks/staging/withdrawals/not_empty.sql",
        "checks/staging/withdrawals/no_duplicate_ids.sql",
        "checks/staging/withdrawals/valid_amount.sql",
        "checks/staging/withdrawals/not_empty_currency.sql",
        "checks/staging/withdrawals/valid_withdrawal_date.sql",
        "checks/staging/withdrawals/player_exists.sql",
        "checks/staging/withdrawals/provider_exists.sql",
        "checks/staging/withdrawals/currency_rate_exists.sql",
    ),
)

GAMES_CONFIG = StagingTableConfig(
    entity_name="games",
    table_name="staging.games",
    build_sql_file="staging/build_games.sql",
    check_sql_files=(
        "checks/staging/games/not_empty.sql",
        "checks/staging/games/no_duplicate_ids.sql",
        "checks/staging/games/valid_amount.sql",
        "checks/staging/games/not_empty_currency.sql",
        "checks/staging/games/valid_game_date.sql",
        "checks/staging/games/player_exists.sql",
        "checks/staging/games/provider_exists.sql",
        "checks/staging/games/game_exists.sql",
        "checks/staging/games/currency_rate_exists.sql",
    ),
)
