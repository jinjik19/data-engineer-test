from dataclasses import dataclass
from pathlib import Path

from de_project.entities.types import EntityType


@dataclass
class SourceEntity:
    name: str
    file_name: str
    entity_type: EntityType
    raw_table: str
    staging_table: str
    required_columns: tuple[str, ...]
    date_column: str | None = None
    date_columns: tuple[str, ...] = ()
    raw_database: str = "raw"
    staging_database: str = "staging"

    def __post_init__(self) -> None:
        if not self.required_columns:
            raise ValueError(
                f"Сущность '{self.name}' должна иметь обязательные колонки"
            )

        if self.entity_type == EntityType.FACT and self.date_column is None:
            raise ValueError(f"Сущность фактов '{self.name}' должна иметь date_column")

    @property
    def raw_full_name(self) -> str:
        return f"{self.raw_database}.{self.raw_table}"

    @property
    def staging_full_name(self) -> str:
        return f"{self.staging_database}.{self.staging_table}"

    def file_path(self, data_dir: Path) -> Path:
        return data_dir / self.file_name
