from pathlib import Path

from de_project.settings import settings
from de_project.dwh.ports import DataWarehouseGateway
from de_project.services.staging.exceptions import (
    DataQualityCheckError,
    SqlFileNotFoundError,
)
from de_project.utils.get_clickhouse_gateway import get_clickhouse_gateway


class SqlScriptRunner:
    def __init__(self, warehouse: DataWarehouseGateway, sql_root: Path) -> None:
        self.warehouse = warehouse
        self.sql_root = sql_root

    def run_file(self, relative_path: str) -> None:
        sql = self._read_sql(relative_path)
        self.warehouse.command(sql)

    def truncate_table(self, table_name: str) -> None:
        self.warehouse.command(f"TRUNCATE TABLE {table_name}")

    def run_check(self, relative_path: str) -> None:
        sql = self._read_sql(relative_path)
        rows = self.warehouse.query_rows(sql)
        bad_rows = rows[0][0]

        if not rows or bad_rows != 0:
            raise DataQualityCheckError(
                f"Проверка качества данных '{relative_path}' вернула ошибку"
            )

    def _read_sql(self, relative_path: str) -> str:
        path = self.sql_root / relative_path

        if not path.exists():
            raise SqlFileNotFoundError(f"SQL файл не найден: {path}")

        return path.read_text(encoding="utf-8").strip()


def create_sql_runner() -> SqlScriptRunner:
    return SqlScriptRunner(
        warehouse=get_clickhouse_gateway(),
        sql_root=settings.sql_dir,
    )
