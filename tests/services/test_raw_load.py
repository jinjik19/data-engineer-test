from datetime import date, datetime, timezone
from pathlib import Path
from uuid import UUID

import pandas as pd
import pytest

from de_project.entities import ENTITIES
from de_project.services.raw.load import EmptySourceDataError, RawLoadService


class FakeWarehouseGateway:
    def __init__(self) -> None:
        self.insert_calls: list[tuple[str, pd.DataFrame]] = []

    def command(self, query: str, parameters: dict | None = None) -> None:
        pass

    def query_rows(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[tuple]:
        return []

    def insert_dataframe(self, table_name: str, dataframe: pd.DataFrame) -> None:
        self.insert_calls.append((table_name, dataframe.copy()))


class FakeRawIngestService:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    def read_source_file(self, entity, data_dir: Path) -> pd.DataFrame:
        return self.dataframe.copy()

    def prepare_raw_dataframe(
        self,
        entity,
        dataframe: pd.DataFrame,
        source_file: str,
        load_id: UUID,
        loaded_at: datetime | None = None,
    ) -> pd.DataFrame:
        prepared_df = dataframe.loc[:, list(entity.required_columns)].copy()
        prepared_df["source_file"] = source_file
        prepared_df["load_id"] = str(load_id)
        prepared_df["loaded_at"] = loaded_at
        return prepared_df


def test_load_fact_entity_to_raw_inserts_data_and_batch_metadata() -> None:
    entity = ENTITIES["deposits"]
    warehouse = FakeWarehouseGateway()

    ingest_service = FakeRawIngestService(
        dataframe=pd.DataFrame(
            {
                "id": [1, 2],
                "player_id": [10, 20],
                "deposit_date": ["2023-01-15", "2023-02-03"],
                "provider_id": [1, 2],
                "amount": [100.0, 250.0],
                "currency": ["USD", "EUR"],
            }
        )
    )

    load_id = UUID("00000000-0000-0000-0000-000000000001")
    loaded_at = datetime(2026, 6, 13, 10, 0, tzinfo=timezone.utc)

    service = RawLoadService(
        warehouse=warehouse,
        ingest_service=ingest_service,
    )

    result = service.load_entity_to_raw(
        entity=entity,
        data_dir=Path("/tmp/data"),
        load_id=load_id,
        loaded_at=loaded_at,
    )

    assert result.entity_name == "deposits"
    assert result.raw_table == "raw.deposits"
    assert result.rows_loaded == 2
    assert result.loaded_months == (
        date(2023, 1, 1),
        date(2023, 2, 1),
    )

    assert len(warehouse.insert_calls) == 2

    raw_table, raw_df = warehouse.insert_calls[0]
    assert raw_table == "raw.deposits"
    assert len(raw_df) == 2
    assert "source_file" in raw_df.columns
    assert "load_id" in raw_df.columns
    assert "loaded_at" in raw_df.columns

    batch_table, batch_df = warehouse.insert_calls[1]
    assert batch_table == "raw.load_batches"
    assert len(batch_df) == 2
    assert set(batch_df["data_month"]) == {
        date(2023, 1, 1),
        date(2023, 2, 1),
    }
    assert set(batch_df["status"]) == {"success"}


def test_load_snapshot_entity_uses_snapshot_batch_date() -> None:
    entity = ENTITIES["players"]
    warehouse = FakeWarehouseGateway()

    ingest_service = FakeRawIngestService(
        dataframe=pd.DataFrame(
            {
                "id": [1],
                "registration_date": ["2023-01-01"],
                "registration_type": ["standard"],
                "country": ["RU"],
            }
        )
    )

    service = RawLoadService(
        warehouse=warehouse,
        ingest_service=ingest_service,
    )

    result = service.load_entity_to_raw(
        entity=entity,
        data_dir=Path("/tmp/data"),
        load_id=UUID("00000000-0000-0000-0000-000000000001"),
        loaded_at=datetime(2026, 6, 13, 10, 0, tzinfo=timezone.utc),
    )

    assert result.loaded_months == (date(1970, 1, 1),)

    _, batch_df = warehouse.insert_calls[1]
    assert batch_df.loc[0, "data_month"] == date(1970, 1, 1)


def test_load_entity_to_raw_fails_for_empty_source_data() -> None:
    entity = ENTITIES["deposits"]
    warehouse = FakeWarehouseGateway()

    ingest_service = FakeRawIngestService(dataframe=pd.DataFrame())

    service = RawLoadService(
        warehouse=warehouse,
        ingest_service=ingest_service,
    )

    with pytest.raises(EmptySourceDataError):
        service.load_entity_to_raw(
            entity=entity,
            data_dir=Path("/tmp/data"),
            load_id=UUID("00000000-0000-0000-0000-000000000001"),
        )

    assert warehouse.insert_calls == []
