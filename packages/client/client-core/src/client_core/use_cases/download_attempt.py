from uuid import UUID
from ..models import FileInfo
from ..ports.incoming.download_attempt import DownloadAttemptPort
from ..ports.outgoing.education import EducationPort
from ..ports.outgoing.local_storage import LocalStoragePort
from ..ports.outgoing.cloud_storage import CloudStoragePort
from ..ports.outgoing.credentials import CredentialsStoragePort
from ..ports.outgoing.crypto import CryptoPort


class DownloadAttemptUseCase(DownloadAttemptPort):
    def __init__(
        self,
        education: EducationPort,
        local_storage: LocalStoragePort,
        cloud_storage: CloudStoragePort,
        credentials: CredentialsStoragePort,
        crypto: CryptoPort,
        credentials_path: str,
    ):
        self.education = education
        self.local_storage = local_storage
        self.cloud_storage = cloud_storage
        self.credentials = credentials
        self.crypto = crypto
        self.credentials_path = credentials_path

    async def __call__(self, attempt_id: UUID, password: str) -> str:
        info = await self.education.get_attempt_download_url(attempt_id)

        _, private_key = self.credentials.load_credentials(
            self.credentials_path, password
        )

        sealed_data = await self.cloud_storage.download(info.url)

        raw_data = self.crypto.unseal(sealed_data, private_key)

        file_info = self.local_storage.write(
            FileInfo(path="", name=info.filename, extension=info.extension),
            raw_data,
        )

        return file_info.path
