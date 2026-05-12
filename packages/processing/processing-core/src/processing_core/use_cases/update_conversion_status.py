from uuid import UUID
from processing_core.ports.incoming.update_conversion_status import (
    UpdateConversionStatusPort,
)
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)


class UpdateConversionStatusUseCase(UpdateConversionStatusPort):
    def __init__(self, repository: ConversionRepositoryPort):
        self._repository = repository

    async def __call__(self, task_id: UUID, status: str) -> None:
        conversion = await self._repository.get_by_task_id(task_id)
        if not conversion:
            # Task might belong to another module or just not a conversion
            return

        await self._repository.update_status(conversion.conversion_id, status)
