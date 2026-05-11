from uuid import UUID
from ..ports.incoming.upload_submission import UploadSubmissionPort
from ..ports.outgoing.submissions import SubmissionsPort
from ..ports.outgoing.file_manager import FileManagerPort


class UploadSubmissionUseCase(UploadSubmissionPort):
    def __init__(self, submissions: SubmissionsPort, file_manager: FileManagerPort):
        self.submissions = submissions
        self.file_manager = file_manager

    async def __call__(self, project_id: UUID, file_path: str) -> None:
        file_info = self.file_manager.get_info(file_path)
        if not self.file_manager.exists(file_info):
            raise FileNotFoundError(f"File not found: {file_path}")

        upload_url, submission_id = await self.submissions.request_upload_url(
            project_id, file_info.extension
        )

        await self.file_manager.upload(upload_url, file_info)

        await self.submissions.commit_submission(submission_id)
