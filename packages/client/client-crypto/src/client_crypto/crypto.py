from typing import override
from shared_kernel import crypto
from client_core.ports.outgoing.crypto import CryptoPort


class CryptoAdapter(CryptoPort):
    @override
    def generate_keypair(self) -> tuple[bytes, bytes]:
        return crypto.generate_keypair()

    @override
    def sign(self, data: bytes, private_key: bytes) -> bytes:
        return crypto.sign(data, private_key_bytes=private_key)
