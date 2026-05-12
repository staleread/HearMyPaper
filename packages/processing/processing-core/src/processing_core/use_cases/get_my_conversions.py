from processing_core.models import Conversion
from processing_core.ports.incoming.get_my_conversions import GetMyConversionsPort
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)


class GetMyConversionsUseCase(GetMyConversionsPort):
    def __init__(self, repository: ConversionRepositoryPort):
        self._repository = repository

    async def __call__(self, subject_id: str) -> list[Conversion]:
        return await self._repository.get_by_subject(subject_id)
