from pathlib import Path

import pytest

from de_project.services.exceptions import DataQualityCheckError, SqlFileNotFoundError
from de_project.services.sql_runner import SqlScriptRunner


class FakeWarehouseGateway:
    def __init__(self, query_result: list[tuple] | None = None) -> None:
        self.query_result = query_result or []
        self.commands: list[str] = []
        self.queries: list[str] = []

    def command(self, query: str, parameters: dict | None = None) -> None:
        self.commands.append(query)

    def query_rows(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[tuple]:
        self.queries.append(query)
        return self.query_result

    def insert_dataframe(self, table_name, dataframe) -> None:
        pass


def test_run_check_accepts_zero_bad_rows(tmp_path: Path) -> None:
    check_path = tmp_path / "check.sql"
    check_path.write_text("SELECT 0", encoding="utf-8")
    warehouse = FakeWarehouseGateway(query_result=[(0,)])

    SqlScriptRunner(warehouse=warehouse, sql_root=tmp_path).run_check("check.sql")

    assert warehouse.queries == ["SELECT 0"]


@pytest.mark.parametrize("query_result", [[], [()], [(2,)]])
def test_run_check_raises_data_quality_error_for_failed_result(
    tmp_path: Path,
    query_result: list[tuple],
) -> None:
    (tmp_path / "check.sql").write_text("SELECT 2", encoding="utf-8")
    warehouse = FakeWarehouseGateway(query_result=query_result)

    with pytest.raises(DataQualityCheckError):
        SqlScriptRunner(warehouse=warehouse, sql_root=tmp_path).run_check("check.sql")


def test_run_file_raises_clear_error_when_sql_file_is_missing(tmp_path: Path) -> None:
    warehouse = FakeWarehouseGateway()

    with pytest.raises(SqlFileNotFoundError, match="missing.sql"):
        SqlScriptRunner(warehouse=warehouse, sql_root=tmp_path).run_file("missing.sql")

    assert warehouse.commands == []
