from typing import override
import jwt
from datetime import datetime, timedelta, timezone

from identity_core.models import AuthUser
from identity_core.ports.outgoing.token_provider import TokenProviderPort, AuthToken


class JwtTokenProviderAdapter(TokenProviderPort):
    def __init__(self, secret: str, lifetime_sec: int, algorithm: str | None = None):
        self.secret = secret
        self.lifetime_sec = lifetime_sec
        self.algorithm = algorithm

    @override
    def create_token(self, user: AuthUser) -> AuthToken:
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.lifetime_sec)

        payload = {
            "sub": user.id,
            "confidentiality_level": user.confidentiality_level.value,
            "integrity_levels": [level.value for level in user.integrity_levels],
            "exp": expires_at,
        }

        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)

        return AuthToken(token=token, expires_at=expires_at)
