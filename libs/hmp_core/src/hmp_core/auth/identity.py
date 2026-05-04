from typing import Annotated

from fastapi import Depends, Header
from pydantic import BaseModel


class IdentityContext(BaseModel):
    """
    Context representing the verified identities of the request.
    Populated from headers injected by Envoy after OPA authorization.
    """
    workload_id: str
    user_pseudonym: str

async def resolve_identity(
    x_spiffe_id: Annotated[str, Header(alias="X-Spiffe-ID")],
    x_user_pseudonym: Annotated[str, Header(alias="X-User-Pseudonym")],
) -> IdentityContext:
    """
    Dependency that extracts trusted identity headers.
    In Zero Trust, we trust these because Envoy/OPA act as the gatekeeper.
    """
    return IdentityContext(
        workload_id=x_spiffe_id,
        user_pseudonym=x_user_pseudonym
    )

IdentityDep = Annotated[IdentityContext, Depends(resolve_identity)]
