from ..ports.incoming.create_user import CreateUserPort
from ..ports.outgoing.identity import IdentityPort
from ..ports.outgoing.credentials import CredentialsStoragePort
from ..ports.outgoing.crypto import CryptoPort
from ..models import User, AccessLevel


class CreateUserUseCase(CreateUserPort):
    def __init__(
        self,
        identity: IdentityPort,
        credentials: CredentialsStoragePort,
        crypto: CryptoPort,
    ):
        self.identity = identity
        self.credentials = credentials
        self.crypto = crypto

    async def __call__(
        self,
        name: str,
        surname: str,
        email: str,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
        credentials_path: str,
        credentials_password: str,
    ) -> User:
        private_key, public_key = self.crypto.generate_keypair()

        user = await self.identity.create_user(
            name=name,
            surname=surname,
            email=email,
            public_key=public_key,
            confidentiality_level=confidentiality_level,
            integrity_levels=integrity_levels,
        )

        self.credentials.save_credentials(
            user_id=user.id,
            path=credentials_path,
            private_key=private_key,
            password=credentials_password,
        )

        return user
