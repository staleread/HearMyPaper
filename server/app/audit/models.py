from pydantic import BaseModel


class ActionLog(BaseModel):
    timestamp: str
    action: str
    is_success: bool
    reason: str | None
