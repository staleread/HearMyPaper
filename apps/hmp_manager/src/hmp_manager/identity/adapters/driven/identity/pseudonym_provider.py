import uidgen
from typing import override

from hmp_manager.identity.domain.ports.outgoing import IdentityProviderPort


class PseudonymIdentityProviderAdapter(IdentityProviderPort):
    @override
    def generate(self) -> str:
        return uidgen.generate()
