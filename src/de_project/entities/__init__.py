from de_project.entities.raw_entity_load_result import RawLoadResultEntity
from de_project.entities.source import SourceEntity
from de_project.entities.types import EntityType


ENTITIES: dict[str, SourceEntity] = {
    "players": SourceEntity(
        name="players",
        file_name="players.csv",
        entity_type=EntityType.REFERENCE,
        raw_table="players",
        staging_table="players",
        required_columns=(
            "id",
            "registration_date",
            "registration_type",
            "country",
        ),
        date_column=None,
    ),
    "providers_map": SourceEntity(
        name="providers_map",
        file_name="providers_map.csv",
        entity_type=EntityType.REFERENCE,
        raw_table="providers_map",
        staging_table="providers_map",
        required_columns=(
            "id",
            "provider_name",
        ),
        date_column=None,
    ),
    "games_map": SourceEntity(
        name="games_map",
        file_name="games_map.csv",
        entity_type=EntityType.REFERENCE,
        raw_table="games_map",
        staging_table="games_map",
        required_columns=(
            "id",
            "game_name",
            "provider_id",
        ),
        date_column=None,
    ),
    "currency_rates": SourceEntity(
        name="currency_rates",
        file_name="currency_rates.csv",
        entity_type=EntityType.FACT,
        raw_table="currency_rates",
        staging_table="currency_rates",
        required_columns=(
            "date",
            "currency",
            "rate_to_usd",
        ),
        date_column="date",
    ),
    "deposits": SourceEntity(
        name="deposits",
        file_name="deposits.csv",
        entity_type=EntityType.FACT,
        raw_table="deposits",
        staging_table="deposits",
        required_columns=(
            "id",
            "player_id",
            "deposit_date",
            "provider_id",
            "amount",
            "currency",
        ),
        date_column="deposit_date",
    ),
    "withdrawals": SourceEntity(
        name="withdrawals",
        file_name="withdrawals.csv",
        entity_type=EntityType.FACT,
        raw_table="withdrawals",
        staging_table="withdrawals",
        required_columns=(
            "id",
            "player_id",
            "withdrawal_date",
            "provider_id",
            "amount",
            "currency",
        ),
        date_column="withdrawal_date",
    ),
    "games": SourceEntity(
        name="games",
        file_name="games.csv",
        entity_type=EntityType.FACT,
        raw_table="games",
        staging_table="games",
        required_columns=(
            "id",
            "player_id",
            "game_date",
            "amount",
            "currency",
            "provider_id",
            "game_id",
        ),
        date_column="game_date",
    ),
}


__all__ = ["SourceEntity", "ENTITIES", "EntityType", "RawLoadResultEntity"]
