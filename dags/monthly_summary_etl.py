from datetime import datetime

from airflow.decorators import dag

from tasks.staging import build_staging_group
from tasks.raw import check_clickhouse_connection, load_raw_entities


@dag(
    dag_id="monthly_summary_etl",
    description="Загрузка сырых данных из CSV файлов, создание staging слоя и построение месячной витрины",
    start_date=datetime(2026, 6, 13),
    schedule="@monthly",
    catchup=False,
    tags=["de-project", "clickhouse", "etl", "monthly_summary"],
    max_active_runs=1,
)
def monthly_summary_etl() -> None:
    clickhouse_ready = check_clickhouse_connection()
    raw_results = load_raw_entities()
    staging_tables = build_staging_group()

    clickhouse_ready >> raw_results >> staging_tables


monthly_summary_etl()
