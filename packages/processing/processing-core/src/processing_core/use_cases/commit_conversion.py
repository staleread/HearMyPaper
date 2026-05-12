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


class CommitConversionUseCase(CommitConversionPort):
    def __init__(
        self,
        repository: ConversionRepositoryPort,
        storage: FileStoragePort,
    ):
        self._repository = repository
        self._storage = storage

    async def __call__(self, command: CommitConversionCommand) -> None:
        conversion = await self._repository.get_conversion(command.conversion_id)
        if not conversion:
            raise ConversionNotFoundError(
                f"Conversion {command.conversion_id} not found"
            )

        if conversion.status != ConversionStatus.PENDING:
            return  # Idempotent

        # Verify file exists in storage (Two-Step Commitment)
        file_path = f"conversions/{command.conversion_id}/source.pdf"
        if not await self._storage.file_exists(file_path):
            raise FileNotUploadedError(
                f"File for conversion {command.conversion_id} not uploaded yet"
            )

        # Mark as committed (Ready for pickup)
        await self._repository.update_status(
            command.conversion_id, ConversionStatus.COMMITTED
        )
