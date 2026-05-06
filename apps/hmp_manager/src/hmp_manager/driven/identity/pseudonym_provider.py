import uidgen
from typing import override

from hmp_manager.domain.user.ports import IdentityProvider


class PseudonymIdentityProvider(IdentityProvider):
    @override
    def generate(self) -> str:
        return uidgen.generate()
