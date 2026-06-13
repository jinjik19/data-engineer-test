from typing import Any

import pandas as pd
from clickhouse_connect.driver.client import Client


class ClickHouseGateway:
    def __init__(self, client: Client) -> None:
        self.client = client

    def command(self, query: str, parameters: dict[str, Any] | None = None) -> None:
        self.client.command(query, parameters=parameters)

    def query_rows(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[tuple[Any, ...]]:
        result = self.client.query(query, parameters=parameters)
        return result.result_rows

    def insert_dataframe(self, table_name: str, dataframe: pd.DataFrame) -> None:
        if dataframe.empty:
            return

        self.client.insert_df(table=table_name, df=dataframe)
