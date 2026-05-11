from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID


class SubmissionStatus(Enum):
    PENDING_UPLOAD = "pending_upload"
    COMMITTED = "committed"
    FAILED = "failed"


@dataclass
class LabSubmission:
    submission_id: UUID
    student_id: str
    project_id: UUID
    storage_path: str
    status: SubmissionStatus
    created_at: datetime
    filename: str
    extension: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class SubmissionListItem:
    submission_id: UUID
    student_id: str
    status: SubmissionStatus
    created_at: datetime
