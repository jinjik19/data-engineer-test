from datetime import datetime, timezone
from uuid import UUID

import pandas as pd
import pytest

from de_project.entities import ENTITIES
from de_project.services.raw.exceptions import MissingColumnsError
from de_project.services.raw.ingest import RawIngestService


def test_prepare_raw_dataframe_adds_metadata_columns() -> None:
    entity = ENTITIES["deposits"]
    service = RawIngestService()

    dataframe = pd.DataFrame(
        {
            "id": [1],
            "player_id": [10],
            "deposit_date": ["2023-01-01"],
            "provider_id": [3],
            "amount": [100.0],
            "currency": ["USD"],
        }
    )

    load_id = UUID("00000000-0000-0000-0000-000000000001")
    loaded_at = datetime(2026, 6, 13, tzinfo=timezone.utc)

    prepared_df = service.prepare_raw_dataframe(
        entity=entity,
        dataframe=dataframe,
        source_file="deposits.csv",
        load_id=load_id,
        loaded_at=loaded_at,
    )

    assert list(prepared_df.columns) == [
        "id",
        "player_id",
        "deposit_date",
        "provider_id",
        "amount",
        "currency",
        "source_file",
        "load_id",
        "loaded_at",
    ]
    assert prepared_df.loc[0, "source_file"] == "deposits.csv"
    assert prepared_df.loc[0, "load_id"] == str(load_id)
    assert prepared_df.loc[0, "loaded_at"] == loaded_at


def test_prepare_raw_dataframe_fails_if_required_column_is_missing() -> None:
    entity = ENTITIES["deposits"]
    service = RawIngestService()

    dataframe = pd.DataFrame(
        {
            "id": [1],
            "player_id": [10],
        }
    )

    with pytest.raises(MissingColumnsError):
        service.prepare_raw_dataframe(
            entity=entity,
            dataframe=dataframe,
            source_file="deposits.csv",
            load_id=UUID("00000000-0000-0000-0000-000000000001"),
        )
