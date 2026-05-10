from uuid import UUID
from ..ports.incoming.view_submission import ViewSubmissionPort
from ..ports.outgoing.download_url_provider import DownloadUrlProviderPort
from ..ports.outgoing.attempt_repository import AttemptRepositoryPort
from ..ports.outgoing.project_repository import ProjectRepositoryPort
from ..exceptions import AccessDeniedError, AttemptNotFoundError, ProjectNotFoundError


class ViewSubmissionUseCase(ViewSubmissionPort):
    def __init__(
        self,
        attempts: AttemptRepositoryPort,
        projects: ProjectRepositoryPort,
        download_url_provider: DownloadUrlProviderPort,
    ):
        self._attempts = attempts
        self._projects = projects
        self._download_url_provider = download_url_provider

    async def __call__(self, instructor_id: str, submission_id: UUID) -> str:
        attempt = await self._attempts.get_by_submission_id(submission_id)
        if not attempt:
            raise AttemptNotFoundError(
                f"Attempt for submission {submission_id} not found"
            )

        project = await self._projects.get_by_id(attempt.project_id)
        if not project:
            raise ProjectNotFoundError(f"Project {attempt.project_id} not found")

        if project.instructor_id != instructor_id:
            raise AccessDeniedError(
                f"Instructor {instructor_id} is not authorized to view submission {submission_id} "
                f"for project {project.id}"
            )

        return await self._download_url_provider.get_download_url(submission_id)
