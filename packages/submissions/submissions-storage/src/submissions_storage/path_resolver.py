from uuid import UUID
from submissions_core.ports.outgoing.path_resolver import FilePathResolverPort


class SubmissionsFilePathResolver(FilePathResolverPort):
    def get_submission_path(
        self, project_id: UUID, student_id: str, submission_id: UUID
    ) -> str:
        return f"{project_id}/{student_id}/{submission_id}.bin"
