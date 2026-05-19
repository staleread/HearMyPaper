from guardpost.authorization import Requirement, AuthorizationContext
from blacksheep import Request
from identity_core.enums import AccessLevel, AccessType
from identity_core.models import AuthUser
from identity_core.ports.incoming import AuthorizeSubjectPort


class BellLaPadulaRequirement(Requirement):
    level: AccessLevel

    def __init__(self, request: Request):
        self.request = request

    def _get_access_type(self, method: str) -> AccessType:
        if method in {"GET", "HEAD", "OPTIONS"}:
            return AccessType.READ
        return AccessType.WRITE

    async def handle(self, context: AuthorizationContext) -> None:
        identity = context.identity

        if identity is None or not identity.is_authenticated():
            return

        claims = identity.claims

        try:
            subject = AuthUser(
                id=str(claims.get("sub") or ""),
                confidentiality_level=AccessLevel(
                    str(claims.get("confidentiality_level") or "UNCLASSIFIED")
                ),
                integrity_levels=[
                    AccessLevel(lvl) for lvl in claims.get("integrity_levels", [])
                ],
            )

            authorize_subject_port = self.request.services.get(AuthorizeSubjectPort)
            access_type = self._get_access_type(self.request.method)

            authorize_subject_port(
                subject,
                access_type=access_type,
                object_access_level=self.level,
            )
            context.succeed(self)
        except Exception:
            return


class UnclassifiedRequirement(BellLaPadulaRequirement):
    level = AccessLevel.UNCLASSIFIED


class ControlledRequirement(BellLaPadulaRequirement):
    level = AccessLevel.CONTROLLED


class RestrictedRequirement(BellLaPadulaRequirement):
    level = AccessLevel.RESTRICTED


class ConfidentialRequirement(BellLaPadulaRequirement):
    level = AccessLevel.CONFIDENTIAL
