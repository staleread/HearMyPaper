from datetime import datetime, UTC
from uuid import uuid4
from processing_core.models import Conversion, ConversionStatus
from processing_core.ports.incoming.request_conversion import (
    RequestConversionPort,
    RequestConversionQuery,
    ConversionResponseDTO,
)
from processing_core.ports.outgoing.resource_broker import ResourceBrokerPort
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)
from processing_core.ports.outgoing.file_storage import FileStoragePort


from processing_core.ports.outgoing.path_resolver import FilePathResolverPort


class RequestConversionUseCase(RequestConversionPort):
    def __init__(
        self,
        broker: ResourceBrokerPort,
        repository: ConversionRepositoryPort,
        storage: FileStoragePort,
        paths: FilePathResolverPort,
    ):
        self._broker = broker
        self._repository = repository
        self._storage = storage
        self._paths = paths

    async def __call__(self, query: RequestConversionQuery) -> ConversionResponseDTO:
        # 1. Acquire task from orchestrator
        assignment = await self._broker.acquire_task(query.task_type.value)

        conversion_id = uuid4()

        # 2. Authorize storage (Blind Handshake)
        # Note the .bin extension as it will be an encrypted file
        file_path = self._paths.get_source_path(conversion_id)
        upload_url = await self._storage.generate_upload_url(file_path)

        # 3. Persist conversion
        now = datetime.now(UTC)
        conversion = Conversion(
            conversion_id=conversion_id,
            source_id=query.source_id,
            subject_id=query.subject_id,
            task_id=assignment.task_id,
            status=ConversionStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        await self._repository.save_conversion(conversion)

        return ConversionResponseDTO(
            conversion_id=conversion_id,
            sealing_key=assignment.sealing_key,
            upload_url=upload_url,
        )
