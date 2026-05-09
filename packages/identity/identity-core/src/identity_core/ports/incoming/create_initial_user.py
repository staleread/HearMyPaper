from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class InitialUserCreateCommand:
    id: str
    name: str
    surname: str
    email: str
    public_key: bytes


class CreateInitialUserPort(Protocol):
    async def __call__(self, cmd: InitialUserCreateCommand) -> bool: ...
