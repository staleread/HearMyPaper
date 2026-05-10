from typing import Protocol
from uuid import UUID


class DownloadUrlProviderPort(Protocol):
    async def get_download_url(self, submission_id: UUID) -> str:
        """Generates a pre-signed download URL for a submission."""
        ...
