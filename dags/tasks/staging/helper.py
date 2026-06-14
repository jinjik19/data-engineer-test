from dataclasses import dataclass
from datetime import timedelta
from typing import Any


from airflow.decorators import task

from de_project.entities.staging_table_config import StagingTableConfig
from de_project.services.staging.sql_runner import create_sql_runner


@dataclass(frozen=True)
class StagingTaskHandles:
    build: Any
    check: Any


@task(execution_timeout=timedelta(minutes=5))
def build_staging_table(table_name: str, build_sql_file: str) -> None:
    runner = create_sql_runner()
    runner.truncate_table(table_name)
    runner.run_file(build_sql_file)


@task(execution_timeout=timedelta(minutes=5))
def run_staging_checks(check_sql_files: list[str]) -> None:
    runner = create_sql_runner()

    for check_sql_file in check_sql_files:
        runner.run_check(check_sql_file)


def create_staging_table_tasks(config: StagingTableConfig) -> StagingTaskHandles:
    build_task = build_staging_table.override(
        task_id=f"build_{config.entity_name}",
    )(
        table_name=config.table_name,
        build_sql_file=config.build_sql_file,
    )

    check_task = run_staging_checks.override(
        task_id=f"check_{config.entity_name}",
    )(
        check_sql_files=list(config.check_sql_files),
    )

    build_task >> check_task

    return StagingTaskHandles(build=build_task, check=check_task)
