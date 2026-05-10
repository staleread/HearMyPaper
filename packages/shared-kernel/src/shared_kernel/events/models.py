from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SubmissionCommittedEvent:
    submission_id: UUID
    student_id: str
    project_id: UUID
    timestamp: datetime
