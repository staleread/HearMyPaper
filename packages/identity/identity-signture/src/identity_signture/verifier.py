from typing import override
from shared_kernel.crypto import verify
from identity_core.ports.outgoing.signature_verifier import SignatureVerifierPort


class SignatureVerifierAdapter(SignatureVerifierPort):
    @override
    def verify(self, challenge: bytes, signature: bytes, public_key: bytes) -> bool:
        return verify(challenge, signature=signature, public_key_bytes=public_key)
