from typing import Protocol


class ChallengeGeneratorPort(Protocol):
    def generate(self) -> bytes: ...
