from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class DownloadInfo:
    url: str
    filename: str
    extension: str


class DownloadUrlProviderPort(Protocol):
    async def get_download_url(self, submission_id: UUID) -> DownloadInfo:
        """Generates a pre-signed download URL for a submission."""
        ...
