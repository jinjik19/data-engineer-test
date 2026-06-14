from dataclasses import dataclass


@dataclass(frozen=True)
class StagingTableConfig:
    entity_name: str
    table_name: str
    build_sql_file: str
    check_sql_files: tuple[str, ...]
