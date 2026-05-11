from typing import Protocol
from uuid import UUID
from ..outgoing.download_url_provider import DownloadInfo


class ViewSubmissionPort(Protocol):
    async def __call__(self, instructor_id: str, attempt_id: UUID) -> DownloadInfo:
        """Returns download info for the given attempt, verifying instructor access."""
        ...
