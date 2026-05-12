from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SubmissionCommittedEvent:
    submission_id: UUID
    student_id: str
    project_id: UUID
    timestamp: datetime


@dataclass(frozen=True, slots=True)
class TaskDispatchedEvent:
    task_id: UUID
    task_type: str
    source_download_url: str
    result_upload_url: str


@dataclass(frozen=True, slots=True)
class TaskStatusUpdatedEvent:
    task_id: UUID
    status: str
