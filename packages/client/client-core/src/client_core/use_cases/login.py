from ..ports.incoming.login import LoginPort
from ..ports.outgoing.crypto import CryptoPort
from ..ports.outgoing.identity import IdentityPort
from ..ports.outgoing.credentials import CredentialsStoragePort
from ..ports.outgoing.session import SessionProviderPort


class LoginUseCase(LoginPort):
    def __init__(
        self,
        identity: IdentityPort,
        credentials: CredentialsStoragePort,
        session_provider: SessionProviderPort,
        crypto: CryptoPort,
    ):
        self.identity = identity
        self.credentials = credentials
        self.session_provider = session_provider
        self.crypto = crypto

    async def __call__(self, token_path: str, password: str) -> None:
        user_id, private_key = self.credentials.load_credentials(token_path, password)

        challenge = await self.identity.init_login(user_id)
        signature = self.crypto.sign(challenge, private_key=private_key)

        token = await self.identity.finalize_login(user_id, challenge, signature)

        self.session_provider.set_token(token)
