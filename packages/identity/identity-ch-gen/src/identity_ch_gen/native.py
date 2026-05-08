import os
from typing import override
from identity_core.ports.outgoing.challenge_generator import ChallengeGeneratorPort


class NativeChallengeGeneratorAdapter(ChallengeGeneratorPort):
    @override
    def generate(self) -> bytes:
        return os.urandom(32)
