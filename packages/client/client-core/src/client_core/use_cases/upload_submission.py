from uuid import UUID
from ..ports.incoming.upload_submission import UploadSubmissionPort
from ..ports.outgoing.submissions import SubmissionsPort
from ..ports.outgoing.local_storage import LocalStoragePort
from ..ports.outgoing.cloud_storage import CloudStoragePort
from ..ports.outgoing.education import EducationPort
from ..ports.outgoing.identity import IdentityPort
from ..ports.outgoing.crypto import CryptoPort


class UploadSubmissionUseCase(UploadSubmissionPort):
    def __init__(
        self,
        submissions: SubmissionsPort,
        education: EducationPort,
        identity: IdentityPort,
        crypto: CryptoPort,
        local_storage: LocalStoragePort,
        cloud_storage: CloudStoragePort,
    ):
        self.submissions = submissions
        self.education = education
        self.identity = identity
        self.crypto = crypto
        self.local_storage = local_storage
        self.cloud_storage = cloud_storage

    async def __call__(self, project_id: UUID, file_path: str) -> None:
        file_info = self.local_storage.get_info(file_path)
        if not self.local_storage.exists(file_info):
            raise FileNotFoundError(f"File not found: {file_path}")

        project = await self.education.get_project(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        instructor_pk = await self.identity.get_public_key(project.instructor_id)

        info = await self.submissions.request_upload_url(
            project_id, file_info.name, file_info.extension
        )

        raw_data = self.local_storage.read(file_info)
        # Seal for instructor
        sealed_data = self.crypto.seal(raw_data, instructor_pk)

        await self.cloud_storage.upload(info.url, sealed_data)

        await self.submissions.commit_submission(info.submission_id)
