from airflow.decorators import task_group

from tasks.staging.currency_rate import build_currency_rates_staging
from tasks.staging.facts import build_facts_staging_group
from tasks.staging.reference import build_reference_staging_group


@task_group(group_id="staging")
def build_staging_group() -> None:
    reference = build_reference_staging_group()
    rates = build_currency_rates_staging()
    facts = build_facts_staging_group()

    [reference, rates] >> facts
