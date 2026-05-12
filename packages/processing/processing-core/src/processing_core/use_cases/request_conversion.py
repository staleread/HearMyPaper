from datetime import datetime, UTC
from processing_core.models import AssignmentDTO, Conversion, ConversionStatus
from processing_core.ports.incoming.request_conversion import (
    RequestConversionPort,
    RequestConversionQuery,
)
from processing_core.ports.outgoing.resource_broker import ResourceBrokerPort
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)
from processing_core.ports.outgoing.file_storage import FileStoragePort


class RequestConversionUseCase(RequestConversionPort):
    def __init__(
        self,
        broker: ResourceBrokerPort,
        repository: ConversionRepositoryPort,
        storage: FileStoragePort,
    ):
        self._broker = broker
        self._repository = repository
        self._storage = storage

    async def __call__(self, query: RequestConversionQuery) -> AssignmentDTO:
        # 1. Acquire compute resource
        assignment = await self._broker.assign_compute_resource(query.task_type)

        # 2. Authorize storage (Blind Handshake)
        # Path format: conversions/{assignment_id}/source.pdf
        file_path = f"conversions/{assignment.assignment_id}/source.pdf"
        upload_url = await self._storage.generate_upload_url(file_path)

        # 3. Persist intent
        now = datetime.now(UTC)
        conversion = Conversion(
            conversion_id=assignment.assignment_id,
            lab_attempt_id=query.lab_attempt_id,
            instructor_id=query.instructor_id,
            worker_id=assignment.worker_id,
            status=ConversionStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        await self._repository.save_conversion(conversion)

        return AssignmentDTO(
            assignment_id=assignment.assignment_id,
            worker_id=assignment.worker_id,
            worker_public_key=assignment.worker_public_key,
            upload_url=upload_url,
            expires_at=assignment.expires_at,
        )
