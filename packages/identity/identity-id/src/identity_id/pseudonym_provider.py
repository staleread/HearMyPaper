import uidgen
from typing import override

from identity_core.ports.outgoing.identity_provider import IdentityProviderPort


class PseudonymIdentityProviderAdapter(IdentityProviderPort):
    @override
    def generate(self) -> str:
        return uidgen.generate()
