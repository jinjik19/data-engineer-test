from airflow.decorators import task_group

from tasks.staging.helper import create_staging_table_tasks
from de_project.services.staging.constants import (
    CURRENCY_RATES_CONFIG,
)


@task_group(group_id="currency_rates")
def build_currency_rates_staging() -> None:
    create_staging_table_tasks(CURRENCY_RATES_CONFIG)
