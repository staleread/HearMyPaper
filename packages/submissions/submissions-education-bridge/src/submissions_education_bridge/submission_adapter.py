from typing import override
from uuid import UUID

from education_core.ports.outgoing.download_url_provider import DownloadUrlProviderPort
from submissions_core.ports.outgoing.submission_repository import (
    SubmissionRepositoryPort,
)
from submissions_core.ports.outgoing.storage import StoragePort


class DownloadUrlProviderAdapter(DownloadUrlProviderPort):
    def __init__(self, submissions: SubmissionRepositoryPort, storage: StoragePort):
        self._submissions = submissions
        self._storage = storage

    @override
    async def get_download_url(self, submission_id: UUID) -> str:
        submission = await self._submissions.find_by_id(submission_id)
        if not submission:
            raise RuntimeError(f"Submission {submission_id} not found")

        return await self._storage.generate_download_url(submission.storage_path)
