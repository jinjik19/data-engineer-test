from airflow.sdk.bases.hook import BaseHook
import clickhouse_connect

from de_project.dwh.clickhouse import ClickHouseGateway
from de_project.settings import Settings, settings


def get_clickhouse_gateway(
    app_settings: Settings = settings,
) -> ClickHouseGateway:
    connection = BaseHook.get_connection(app_settings.clickhouse_conn_id)

    client = clickhouse_connect.get_client(
        host=connection.host,
        port=connection.port or 8123,
        username=connection.login,
        password=connection.password,
        database=connection.schema or app_settings.raw_database,
    )

    return ClickHouseGateway(client=client)
