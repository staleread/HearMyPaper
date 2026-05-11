from typing import Protocol


class CryptoPort(Protocol):
    def generate_keypair(self) -> tuple[bytes, bytes]:
        """Generates a new private/public key pair. Returns (private_key, public_key)."""
        ...

    def sign(self, data: bytes, private_key: bytes) -> bytes:
        """Signs the data with the given private key. Returns the signature."""
        ...
