from datetime import timedelta

from airflow.decorators import task, task_group

from de_project.services.mart.constants import MONTHLY_SUMMARY_CHECKS
from de_project.services.sql_runner import create_sql_runner


@task(execution_timeout=timedelta(minutes=5))
def build_monthly_summary() -> None:
    runner = create_sql_runner()
    runner.truncate_table("mart.monthly_summary")
    runner.run_file("mart/build_monthly_summary.sql")


@task(execution_timeout=timedelta(minutes=3))
def check_monthly_summary() -> None:
    runner = create_sql_runner()

    for check_file in MONTHLY_SUMMARY_CHECKS:
        runner.run_check(check_file)


@task_group(group_id="mart")
def build_mart_group() -> None:
    build = build_monthly_summary()
    check = check_monthly_summary()

    build >> check
