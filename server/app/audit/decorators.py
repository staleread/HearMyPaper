from functools import wraps
from typing import Callable, Awaitable, TypeVar, ParamSpec
from fastapi import HTTPException

from app.shared.utils.db import SqlRunner
from . import service as audit_service

P = ParamSpec("P")
R = TypeVar("R")


def audit() -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorator for FastAPI route handlers that logs all actions to the audit log.
    Captures the function name as action, wraps in try-except to determine success,
    and logs HTTPException details as reason.
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            action = func.__name__
            db = kwargs.get("db")

            if not isinstance(db, SqlRunner):
                raise RuntimeError(
                    f"Function {func.__name__} must have 'db' parameter of type SqlRunner for audit"
                )

            try:
                result = await func(*args, **kwargs)
                audit_service.add_action_log(
                    action=action, is_success=True, reason=None, db=db
                )
                return result
            except HTTPException as e:
                audit_service.add_action_log(
                    action=action, is_success=False, reason=e.detail, db=db
                )
                raise
            except Exception as e:
                audit_service.add_action_log(
                    action=action, is_success=False, reason=str(e), db=db
                )
                raise

        return wrapper

    return decorator
