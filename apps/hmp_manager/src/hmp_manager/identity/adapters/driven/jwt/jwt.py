from typing import override
import jwt
from datetime import datetime, timedelta, timezone

from hmp_manager.config import get_settings
from hmp_manager.identity.domain.models import AuthUser
from hmp_manager.identity.domain.ports.incoming import AuthToken
from hmp_manager.identity.domain.ports.outgoing import TokenProviderPort


class JwtTokenProviderAdapter(TokenProviderPort):
    @override
    def create_token(self, user: AuthUser) -> AuthToken:
        settings = get_settings().jwt

        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=settings.lifetime_sec
        )

        payload = {
            "sub": user.id,
            "confidentiality_level": user.confidentiality_level.value,
            "integrity_levels": [level.value for level in user.integrity_levels],
            "exp": expires_at,
        }

        token = jwt.encode(payload, settings.secret, algorithm=settings.algorithm)

        return AuthToken(token=token, expires_at=expires_at)
