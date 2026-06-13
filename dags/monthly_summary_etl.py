from datetime import datetime
from uuid import uuid4

from airflow.decorators import dag, task

from de_project.utils.get_clickhouse_gateway import get_clickhouse_gateway
from de_project.services.raw.pipeline import RawPipelineService
from de_project.settings import settings


@dag(
    dag_id="monthly_summary_etl",
    description="Загрузка сырых данных из CSV файлов, создание staging слоя и построение месячной витрины",
    start_date=datetime(2026, 6, 13),
    schedule="@monthly",
    catchup=False,
    tags=["de-project", "clickhouse", "etl", "monthly_summary"],
)
def raw_ingest_dag() -> None:
    @task
    def check_clickhouse_connection() -> None:
        gateway = get_clickhouse_gateway()
        result = gateway.query_rows("SELECT 1")

        if not result or result[0][0] != 1:
            raise RuntimeError(f"Неожиданный ответ ClickHouse: {result}")

    @task
    def load_raw_entities() -> list[dict]:
        load_id = str(uuid4())

        gateway = get_clickhouse_gateway()
        pipeline = RawPipelineService(warehouse=gateway)

        results = pipeline.load_all_entities_to_raw(
            data_dir=settings.data_dir,
            load_id=uuid4() if not load_id else __import__("uuid").UUID(load_id),
        )

        return [
            {
                "entity_name": result.entity_name,
                "raw_table": result.raw_table,
                "source_file": result.source_file,
                "rows_loaded": result.rows_loaded,
                "loaded_months": [month.isoformat() for month in result.loaded_months],
                "load_id": str(result.load_id),
            }
            for result in results
        ]

    clickhouse_ready = check_clickhouse_connection()
    raw_results = load_raw_entities()

    clickhouse_ready >> raw_results


raw_ingest_dag()
