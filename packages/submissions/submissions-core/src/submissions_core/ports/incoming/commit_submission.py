from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class CommitSubmissionCommand:
    submission_id: UUID
    student_id: str


class CommitSubmissionPort(Protocol):
    async def __call__(self, cmd: CommitSubmissionCommand) -> None: ...
