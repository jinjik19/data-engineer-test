from pathlib import Path
from uuid import UUID

from de_project.entities import ENTITIES, RawLoadResultEntity, SourceEntity
from de_project.dwh.ports import DataWarehouseGateway
from de_project.services.raw.load import RawLoadService


class RawPipelineService:
    def __init__(
        self,
        warehouse: DataWarehouseGateway,
        raw_load_service: RawLoadService | None = None,
    ) -> None:
        self.warehouse = warehouse
        self.raw_load_service = raw_load_service or RawLoadService(
            warehouse=warehouse,
        )

    def load_all_entities_to_raw(
        self,
        data_dir: Path,
        load_id: UUID,
        entities: dict[str, SourceEntity] = ENTITIES,
    ) -> list[RawLoadResultEntity]:
        results: list[RawLoadResultEntity] = []

        for entity in entities.values():
            result = self.raw_load_service.load_entity_to_raw(
                entity=entity,
                data_dir=data_dir,
                load_id=load_id,
            )
            results.append(result)

        return results
