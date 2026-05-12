from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CommitConversionCommand:
    conversion_id: UUID


class CommitConversionPort(Protocol):
    async def __call__(self, command: CommitConversionCommand) -> None: ...
