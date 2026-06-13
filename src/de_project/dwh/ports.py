from typing import Any, Protocol

import pandas as pd


class DataWarehouseGateway(Protocol):
    def command(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> None: ...

    def query_rows(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[tuple[Any, ...]]: ...

    def insert_dataframe(
        self,
        table_name: str,
        dataframe: pd.DataFrame,
    ) -> None: ...
