from typing import Protocol


class LoginPort(Protocol):
    async def __call__(self, token_path: str, password: str) -> None: ...
