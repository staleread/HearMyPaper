from ..ports.incoming.login import LoginPort
from ..ports.outgoing.identity import IdentityPort
from ..ports.outgoing.credentials import CredentialsStoragePort
from ..ports.outgoing.session import SessionProviderPort
from shared_kernel import crypto


class LoginUseCase(LoginPort):
    def __init__(
        self,
        identity_port: IdentityPort,
        credentials_port: CredentialsStoragePort,
        session_provider: SessionProviderPort,
    ):
        self.identity_port = identity_port
        self.credentials_port = credentials_port
        self.session_provider = session_provider

    async def __call__(self, token_path: str, password: str) -> None:
        user_id, private_key = self.credentials_port.load_credentials(
            token_path, password
        )

        challenge = await self.identity_port.init_login(user_id)
        signature = crypto.sign(challenge, private_key_bytes=private_key)

        token = await self.identity_port.finalize_login(user_id, challenge, signature)

        self.session_provider.set_token(token)
