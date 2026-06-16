from airflow.decorators import task_group
from tasks.staging.helper import create_staging_table_tasks

from de_project.services.staging.constants import (
    DEPOSITS_CONFIG,
    GAMES_CONFIG,
    WITHDRAWALS_CONFIG,
)


@task_group(group_id="facts_staging")
def build_facts_staging_group() -> None:
    create_staging_table_tasks(DEPOSITS_CONFIG)
    create_staging_table_tasks(WITHDRAWALS_CONFIG)
    create_staging_table_tasks(GAMES_CONFIG)
