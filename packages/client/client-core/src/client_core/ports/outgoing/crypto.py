from typing import Protocol


class CryptoPort(Protocol):
    def generate_keypair(self) -> tuple[bytes, bytes]:
        """Generates a new private/public key pair. Returns (private_key, public_key)."""
        ...

    def sign(self, data: bytes, private_key: bytes) -> bytes:
        """Signs the data with the given private key. Returns the signature."""
        ...

    def seal(self, data: bytes, public_key: bytes) -> bytes:
        """Encrypts data for a recipient using their public key."""
        ...

    def unseal(self, data: bytes, private_key: bytes) -> bytes:
        """Decrypts data using the recipient's private key."""
        ...
