from typing import Protocol


class IdentityProviderPort(Protocol):
    def generate(self) -> str: ...
