from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from .enums import AccessLevel
from .utils import (
    authorize_composite_identity,
    resolve_access_type,
    resolve_user_access_claims,
    resolve_workload_access_claims,
)

P = ParamSpec("P")
R = TypeVar("R")


def authorize(
    access_level: AccessLevel,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorator for FastAPI route handlers that enforces Stacked Authorization.
    - Infers `access_type` from the verb part of the function name.
    - Verifies the Workload identity (SPIFFE ID) from the request state.
    - Verifies the User identity (Subject) from the injected dependency.
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            func_name = getattr(func, "__name__", str(func))
            access_type = resolve_access_type(func_name)

            user_claims = resolve_user_access_claims(kwargs)
            workload_claims = await resolve_workload_access_claims(kwargs)

            authorize_composite_identity(
                workload_claims=workload_claims,
                user_claims=user_claims,
                access_type=access_type,
                object_access_level=access_level,
            )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
