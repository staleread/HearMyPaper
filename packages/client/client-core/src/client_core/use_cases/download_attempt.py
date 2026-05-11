from uuid import UUID
from ..ports.incoming.download_attempt import DownloadAttemptPort
from ..ports.outgoing.education import EducationPort
from ..ports.outgoing.file_manager import FileManagerPort


class DownloadAttemptUseCase(DownloadAttemptPort):
    def __init__(self, education: EducationPort, file_manager: FileManagerPort):
        self.education = education
        self.file_manager = file_manager

    async def __call__(self, attempt_id: UUID, download_folder: str) -> str:
        download_url = await self.education.get_attempt_download_url(attempt_id)

        file_info = await self.file_manager.download(
            url=download_url,
            folder=download_folder,
            name=f"attempt_{attempt_id}",
            extension="pdf",
        )

        return file_info.path
