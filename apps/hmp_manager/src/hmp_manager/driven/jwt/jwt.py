from typing import override
import jwt
from datetime import datetime, timedelta, timezone

from hmp_manager.config import get_settings
from hmp_manager.domain.auth.models import AuthUser, AuthToken
from hmp_manager.domain.auth.ports import TokenProvider


class JwtTokenProvider(TokenProvider):
    @override
    def create_token(self, user: AuthUser) -> AuthToken:
        settings = get_settings()
        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=settings.jwt_lifetime_sec
        )

        payload = {
            "sub": user.id,
            "confidentiality_level": user.confidentiality_level.value,
            "integrity_levels": [level.value for level in user.integrity_levels],
            "exp": expires_at,
        }

        token = jwt.encode(
            payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
        )

        return AuthToken(token=token, expires_at=expires_at)
