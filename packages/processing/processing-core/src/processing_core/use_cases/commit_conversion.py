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
from processing_core.ports.outgoing.path_resolver import FilePathResolverPort


class CommitConversionUseCase(CommitConversionPort):
    def __init__(
        self,
        repository: ConversionRepositoryPort,
        storage: FileStoragePort,
        broker: ResourceBrokerPort,
        identity: IdentityPort,
        paths: FilePathResolverPort,
    ):
        self._repository = repository
        self._storage = storage
        self._broker = broker
        self._identity = identity
        self._paths = paths

    async def __call__(self, command: CommitConversionCommand) -> None:
        print(
            f"[DEBUG] Executing CommitConversionUseCase for conversion {command.conversion_id}"
        )
        conversion = await self._repository.get_conversion(command.conversion_id)
        if not conversion:
            print(f"[ERROR] Conversion {command.conversion_id} not found")
            raise ConversionNotFoundError(
                f"Conversion {command.conversion_id} not found"
            )

        if conversion.status != ConversionStatus.PENDING:
            print(
                f"[WARN] Conversion {command.conversion_id} is in status {conversion.status}, skipping commit"
            )
            return

        # Verify source file exists (.bin extension)
        source_path = self._paths.get_source_path(conversion.conversion_id)
        if not await self._storage.file_exists(source_path):
            print(f"[ERROR] Source file not found: {source_path}")
            raise FileNotUploadedError(
                f"Source file for conversion {conversion.conversion_id} not found"
            )

        # Generate URLs for the worker
        print(f"[DEBUG] Generating URLs for conversion {command.conversion_id}")
        source_url = await self._storage.generate_download_url(source_path)

        # Result will also be encrypted .bin
        result_path = self._paths.get_result_path(conversion.conversion_id)
        result_url = await self._storage.generate_upload_url(result_path)

        # Get subject's public key to seal the result for
        print(f"[DEBUG] Fetching public key for subject {conversion.subject_id}")
        sealing_key = await self._identity.get_public_key(conversion.subject_id)

        # Start the task in the orchestrator
        print(f"[DEBUG] Dispatching task {conversion.task_id} to broker")
        await self._broker.start_task(
            task_id=conversion.task_id,
            source_download_url=source_url,
            result_upload_url=result_url,
            sealing_key=sealing_key,
        )

        # Mark as committed
        print(
            f"[DEBUG] Updating status for conversion {command.conversion_id} to COMMITTED"
        )
        await self._repository.update_status(
            command.conversion_id, ConversionStatus.COMMITTED
        )
