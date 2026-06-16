from datetime import timedelta
from uuid import uuid4

from airflow.decorators import task

from de_project.services.raw.pipeline import RawPipelineService
from de_project.settings import settings
from de_project.utils.get_clickhouse_gateway import get_clickhouse_gateway


@task(execution_timeout=timedelta(minutes=1))
def check_clickhouse_connection() -> None:
    gateway = get_clickhouse_gateway()
    result = gateway.query_rows("SELECT 1")

    if not result or result[0][0] != 1:
        raise RuntimeError(f"Неожиданный ответ ClickHouse: {result}")


@task(execution_timeout=timedelta(minutes=5))
def load_raw_entities() -> list[dict]:
    load_id = str(uuid4())

    gateway = get_clickhouse_gateway()
    pipeline = RawPipelineService(warehouse=gateway)

    results = pipeline.load_all_entities_to_raw(
        data_dir=settings.data_dir,
        load_id=load_id,
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
