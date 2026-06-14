from airflow.decorators import task_group

from tasks.staging.helper import create_staging_table_tasks
from de_project.services.staging.constants import (
    GAMES_MAP_CONFIG,
    PLAYERS_CONFIG,
    PROVIDERS_MAP_CONFIG,
)


@task_group(group_id="reference_staging")
def build_reference_staging_group() -> None:
    create_staging_table_tasks(PLAYERS_CONFIG)
    providers_map = create_staging_table_tasks(PROVIDERS_MAP_CONFIG)
    games_map = create_staging_table_tasks(GAMES_MAP_CONFIG)

    providers_map.check >> games_map.build
