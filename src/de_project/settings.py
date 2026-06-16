import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    sql_dir: Path
    clickhouse_conn_id: str
    raw_database: str
    staging_database: str
    mart_database: str


def get_settings() -> Settings:
    return Settings(
        data_dir=Path(os.getenv("DATA_DIR", "/opt/airflow/data")),
        sql_dir=Path(os.getenv("DE_PROJECT_SQL_DIR", "/opt/airflow/sql")),
        clickhouse_conn_id=os.getenv(
            "CLICKHOUSE_CONN_ID",
            "clickhouse_default",
        ),
        raw_database=os.getenv("RAW_DATABASE", "raw"),
        staging_database=os.getenv("STAGING_DATABASE", "staging"),
        mart_database=os.getenv("MART_DATABASE", "mart"),
    )


settings = get_settings()
