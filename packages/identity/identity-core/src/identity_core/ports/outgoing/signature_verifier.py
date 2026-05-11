from typing import Protocol


class SignatureVerifierPort(Protocol):
    def verify(self, challenge: bytes, signature: bytes, public_key: bytes) -> bool: ...
