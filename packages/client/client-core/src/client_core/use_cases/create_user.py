from ..ports.incoming.create_user import CreateUserPort
from ..ports.outgoing.identity import IdentityPort
from ..ports.outgoing.credentials import CredentialsStoragePort
from ..models import User, AccessLevel
from shared_kernel import crypto


class CreateUserUseCase(CreateUserPort):
    def __init__(
        self, identity_port: IdentityPort, credentials_port: CredentialsStoragePort
    ):
        self.identity_port = identity_port
        self.credentials_port = credentials_port

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
        # Generate key pair
        private_key, public_key = crypto.generate_keypair()

        # Create user on server
        user = await self.identity_port.create_user(
            name=name,
            surname=surname,
            email=email,
            public_key=public_key,
            confidentiality_level=confidentiality_level,
            integrity_levels=integrity_levels,
        )

        # Save credentials locally
        self.credentials_port.save_credentials(
            user_id=user.id,
            path=credentials_path,
            private_key=private_key,
            password=credentials_password,
        )

        return user
