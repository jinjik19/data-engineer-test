from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class RawLoadResultEntity:
    entity_name: str
    raw_table: str
    source_file: str
    rows_loaded: int
    loaded_months: tuple[date, ...]
    load_id: UUID
