from processing_core.exceptions import (
    ConversionNotFoundError,
    FileNotUploadedError,
)
from processing_core.models import ConversionStatus
from processing_core.ports.incoming.commit_conversion import (
    CommitConversionPort,
    CommitConversionCommand,
)
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)
from processing_core.ports.outgoing.file_storage import FileStoragePort
from processing_core.ports.outgoing.resource_broker import ResourceBrokerPort
from processing_core.ports.outgoing.identity import IdentityPort


class CommitConversionUseCase(CommitConversionPort):
    def __init__(
        self,
        repository: ConversionRepositoryPort,
        storage: FileStoragePort,
        broker: ResourceBrokerPort,
        identity: IdentityPort,
    ):
        self._repository = repository
        self._storage = storage
        self._broker = broker
        self._identity = identity

    async def __call__(self, command: CommitConversionCommand) -> None:
        conversion = await self._repository.get_conversion(command.conversion_id)
        if not conversion:
            raise ConversionNotFoundError(
                f"Conversion {command.conversion_id} not found"
            )

        if conversion.status != ConversionStatus.PENDING:
            return

        # Verify source file exists (.bin extension)
        source_path = f"conversions/{conversion.conversion_id}/source.pdf.bin"
        if not await self._storage.file_exists(source_path):
            raise FileNotUploadedError(
                f"Source file for conversion {conversion.conversion_id} not found"
            )

        # Generate URLs for the worker
        source_url = await self._storage.generate_download_url(source_path)

        # Result will also be encrypted .bin
        result_path = f"conversions/{conversion.conversion_id}/result.mp3.bin"
        result_url = await self._storage.generate_upload_url(result_path)

        # Get subject's public key to seal the result for
        sealing_key = await self._identity.get_public_key(conversion.subject_id)

        # Start the task in the orchestrator
        await self._broker.start_task(
            task_id=conversion.task_id,
            source_download_url=source_url,
            result_upload_url=result_url,
            sealing_key=sealing_key,
        )

        # Mark as committed
        await self._repository.update_status(
            command.conversion_id, ConversionStatus.COMMITTED
        )
