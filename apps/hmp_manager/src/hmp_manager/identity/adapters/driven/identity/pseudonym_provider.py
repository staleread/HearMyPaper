import uidgen
from typing import override

from hmp_manager.identity.domain.ports import IdentityProvider


class PseudonymIdentityProvider(IdentityProvider):
    @override
    def generate(self) -> str:
        return uidgen.generate()
