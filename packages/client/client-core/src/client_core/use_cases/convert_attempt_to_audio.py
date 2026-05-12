from uuid import UUID
from ..ports.incoming.convert_attempt_to_audio import ConvertAttemptToAudioPort
from ..ports.outgoing.processing import ProcessingPort
from ..ports.outgoing.local_storage import LocalStoragePort
from ..ports.outgoing.cloud_storage import CloudStoragePort
from ..ports.outgoing.crypto import CryptoPort
from ..models import ProcessingTaskType


class ConvertAttemptToAudioUseCase(ConvertAttemptToAudioPort):
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

    async def __call__(self, attempt_id: UUID, file_path: str) -> None:
        file_info = self.local_storage.get_info(file_path)
        if not self.local_storage.exists(file_info):
            raise FileNotFoundError(f"File not found: {file_path}")

        # 1. Request conversion
        info = await self.processing.request_conversion(
            attempt_id, ProcessingTaskType.PDF_TO_AUDIO
        )

        # 2. Read local attempt file
        raw_data = self.local_storage.read(file_info)

        # 3. Seal with worker's public key
        sealed_data = self.crypto.seal(raw_data, info.worker_public_key)

        # 4. Upload to cloud storage
        await self.cloud_storage.upload(info.upload_url, sealed_data)

        # 5. Commit conversion
        await self.processing.commit_conversion(info.conversion_id)
