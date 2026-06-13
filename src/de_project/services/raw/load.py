from datetime import date, datetime, timezone
from pathlib import Path
from uuid import UUID

import pandas as pd

from de_project.dwh.ports import DataWarehouseGateway
from de_project.entities import SourceEntity, RawLoadResultEntity, EntityType
from de_project.services.raw.exceptions import EmptySourceDataError, RawLoadError
from de_project.services.raw.ingest import RawIngestService


REFERENCE_LOADED_DATE = date(1970, 1, 1)


class RawLoadService:
    def __init__(
        self,
        warehouse: DataWarehouseGateway,
        ingest_service: RawIngestService | None = None,
    ) -> None:
        self.warehouse = warehouse
        self.ingest_service = ingest_service or RawIngestService()

    def load_entity_to_raw(
        self,
        entity: SourceEntity,
        data_dir: Path,
        load_id: UUID,
        loaded_at: datetime | None = None,
    ) -> RawLoadResultEntity:
        loaded_at = loaded_at or datetime.now(timezone.utc)
        source_df = self._get_source_df(entity, data_dir)

        prepared_df = self.ingest_service.prepare_raw_dataframe(
            entity=entity,
            dataframe=source_df,
            source_file=entity.file_name,
            load_id=load_id,
            loaded_at=loaded_at,
        )

        self.warehouse.insert_dataframe(
            table_name=entity.raw_full_name,
            dataframe=prepared_df,
        )

        loaded_months = self._get_loaded_months(
            entity=entity,
            dataframe=prepared_df,
        )

        self._register_successful_batches(
            entity=entity,
            loaded_months=loaded_months,
            source_file=entity.file_name,
            load_id=load_id,
            loaded_at=loaded_at,
        )

        return RawLoadResultEntity(
            entity_name=entity.name,
            raw_table=entity.raw_full_name,
            source_file=entity.file_name,
            rows_loaded=len(prepared_df),
            loaded_months=loaded_months,
            load_id=load_id,
        )

    def _get_source_df(self, entity: SourceEntity, data_dir: Path) -> pd.DataFrame:
        source_df = self.ingest_service.read_source_file(
            entity=entity,
            data_dir=data_dir,
        )
        if source_df.empty:
            raise EmptySourceDataError(
                f"Файл источника для сущности '{entity.name}' пуст"
            )

        return source_df

    def _get_loaded_months(
        self,
        entity: SourceEntity,
        dataframe: pd.DataFrame,
    ) -> tuple[date, ...]:
        if entity.entity_type == EntityType.REFERENCE:
            return (REFERENCE_LOADED_DATE,)

        if entity.date_column is None:
            raise RawLoadError(
                f"Сущность фактов '{entity.name}' должна содержать date_column"
            )

        month_values = (
            pd.to_datetime(dataframe[entity.date_column], errors="raise")
            .dt.to_period("M")
            .dt.to_timestamp()
            .dt.date.unique()
        )

        return tuple(sorted(month_values))

    def _register_successful_batches(
        self,
        entity: SourceEntity,
        loaded_months: tuple[date, ...],
        source_file: str,
        load_id: UUID,
        loaded_at: datetime,
    ) -> None:
        batch_df = pd.DataFrame(
            {
                "entity": [entity.name for _ in loaded_months],
                "data_month": list(loaded_months),
                "load_id": [str(load_id) for _ in loaded_months],
                "source_file": [source_file for _ in loaded_months],
                "loaded_at": [loaded_at for _ in loaded_months],
                "status": ["success" for _ in loaded_months],
            }
        )

        self.warehouse.insert_dataframe(
            table_name="raw.load_batches",
            dataframe=batch_df,
        )
