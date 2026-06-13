import os
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    clickhouse_conn_id: str
    raw_database: str
    staging_database: str
    mart_database: str


def get_settings() -> Settings:
    return Settings(
        data_dir=Path(os.getenv("DATA_DIR", "/opt/airflow/data")),
        clickhouse_conn_id=os.getenv(
            "CLICKHOUSE_CONN_ID",
            "clickhouse_default",
        ),
        raw_database=os.getenv("RAW_DATABASE", "raw"),
        staging_database=os.getenv("STAGING_DATABASE", "staging"),
        mart_database=os.getenv("MART_DATABASE", "mart"),
    )


settings = get_settings()
