from uuid import UUID
from processing_core.exceptions import (
    ConversionNotFoundError,
    FileNotUploadedError,
    InvalidConversionStatusError,
)
from processing_core.models import ConversionStatus
from processing_core.ports.incoming.get_conversion_download_url import (
    GetConversionDownloadUrlPort,
)
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)
from processing_core.ports.outgoing.file_storage import FileStoragePort


class GetConversionDownloadUrlUseCase(GetConversionDownloadUrlPort):
    def __init__(
        self,
        repository: ConversionRepositoryPort,
        storage: FileStoragePort,
    ):
        self._repository = repository
        self._storage = storage

    async def __call__(self, conversion_id: UUID) -> str:
        conversion = await self._repository.get_conversion(conversion_id)
        if not conversion:
            raise ConversionNotFoundError(f"Conversion {conversion_id} not found")

        if conversion.status != ConversionStatus.COMPLETED:
            raise InvalidConversionStatusError(
                f"Conversion {conversion_id} is in status {conversion.status}, but COMPLETED is required."
            )

        result_path = f"conversions/{conversion.conversion_id}/result.mp3.bin"
        if not await self._storage.file_exists(result_path):
            raise FileNotUploadedError(
                f"Conversion result file for {conversion_id} not found"
            )

        return await self._storage.generate_download_url(result_path)
