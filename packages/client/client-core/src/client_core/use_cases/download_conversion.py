from uuid import UUID
from ..ports.incoming.download_conversion import DownloadConversionPort
from ..ports.outgoing.processing import ProcessingPort
from ..ports.outgoing.local_storage import LocalStoragePort
from ..ports.outgoing.cloud_storage import CloudStoragePort
from ..ports.outgoing.credentials import CredentialsStoragePort
from ..ports.outgoing.crypto import CryptoPort


class DownloadConversionUseCase(DownloadConversionPort):
    def __init__(
        self,
        processing: ProcessingPort,
        local_storage: LocalStoragePort,
        cloud_storage: CloudStoragePort,
        credentials: CredentialsStoragePort,
        crypto: CryptoPort,
        credentials_path: str,
    ):
        self.processing = processing
        self.local_storage = local_storage
        self.cloud_storage = cloud_storage
        self.credentials = credentials
        self.crypto = crypto
        self.credentials_path = credentials_path

    async def __call__(self, conversion_id: UUID, password: str) -> str:
        download_url = await self.processing.get_conversion_download_url(conversion_id)

        sealed_data = await self.cloud_storage.download(download_url)

        user_id, private_key = self.credentials.load_credentials(
            self.credentials_path, password
        )

        raw_data = self.crypto.unseal(sealed_data, private_key)

        filename = f"conversion_{conversion_id}.mp3"
        file_info = self.local_storage.get_info(filename)
        self.local_storage.write(file_info, raw_data)

        return file_info.path
