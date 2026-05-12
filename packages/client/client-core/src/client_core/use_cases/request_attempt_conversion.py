from uuid import UUID
from ..ports.incoming.request_attempt_conversion import RequestAttemptConversionPort
from ..ports.outgoing.processing import ProcessingPort
from ..ports.outgoing.local_storage import LocalStoragePort
from ..ports.outgoing.cloud_storage import CloudStoragePort
from ..ports.outgoing.crypto import CryptoPort
from ..models import ProcessingTaskType


class RequestAttemptConversionUseCase(RequestAttemptConversionPort):
    def __init__(
        self,
        processing: ProcessingPort,
        crypto: CryptoPort,
        local_storage: LocalStoragePort,
        cloud_storage: CloudStoragePort,
    ):
        self.processing = processing
        self.crypto = crypto
        self.local_storage = local_storage
        self.cloud_storage = cloud_storage

    async def __call__(self, source_id: UUID, file_path: str) -> None:
        file_info = self.local_storage.get_info(file_path)
        if not self.local_storage.exists(file_info):
            raise FileNotFoundError(f"File not found: {file_path}")

        info = await self.processing.request_conversion(
            source_id, ProcessingTaskType.PDF_TO_AUDIO
        )

        raw_data = self.local_storage.read(file_info)

        sealed_data = self.crypto.seal(raw_data, info.sealing_key)

        await self.cloud_storage.upload(info.upload_url, sealed_data)

        await self.processing.commit_conversion(info.conversion_id)
