from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

import pandas as pd

from de_project.entities import SourceEntity
from de_project.services.raw.exceptions import (
    MissingColumnsError,
    SourceFileNotFoundError,
)


class RawIngestService:
    def read_source_file(self, entity: SourceEntity, data_dir: Path) -> pd.DataFrame:
        file_path = entity.file_path(data_dir)

        if not file_path.exists():
            raise SourceFileNotFoundError(f"Файл не найден: {file_path}")

        return pd.read_csv(file_path)

    def validate_required_columns(
        self,
        entity: SourceEntity,
        dataframe: pd.DataFrame,
    ) -> None:
        missing_columns = set(entity.required_columns) - set(dataframe.columns)

        if missing_columns:
            raise MissingColumnsError(
                f"Нет объязательного поле '{entity.name}': {sorted(missing_columns)}"
            )

    def prepare_raw_dataframe(
        self,
        entity: SourceEntity,
        dataframe: pd.DataFrame,
        source_file: str,
        load_id: UUID,
        loaded_at: datetime | None = None,
    ) -> pd.DataFrame:
        self.validate_required_columns(entity, dataframe)

        prepared_df = dataframe.loc[:, list(entity.required_columns)].copy()

        for column in entity.date_columns:
            prepared_df[column] = pd.to_datetime(
                prepared_df[column],
                errors="raise",
            ).dt.date

        prepared_df["source_file"] = source_file
        prepared_df["load_id"] = str(load_id)
        prepared_df["loaded_at"] = loaded_at or datetime.now(timezone.utc)

        return prepared_df
