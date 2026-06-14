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
