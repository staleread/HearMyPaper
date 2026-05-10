from uuid import UUID
from pathlib import Path
from ..ports.incoming.upload_submission import UploadSubmissionPort
from ..ports.outgoing.submissions import SubmissionsPort
import httpx


class UploadSubmissionUseCase(UploadSubmissionPort):
    def __init__(self, submissions_port: SubmissionsPort):
        self.submissions_port = submissions_port

    async def __call__(self, project_id: UUID, file_path: str) -> None:
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = p.suffix.lstrip(".")

        # 1. Request upload URL and submission ID
        upload_url, submission_id = await self.submissions_port.request_upload_url(
            project_id, file_extension
        )

        # 2. Upload file directly to storage
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as f:
                response = await client.put(upload_url, content=f)
                response.raise_for_status()

        # 3. Commit submission
        await self.submissions_port.commit_submission(submission_id)
