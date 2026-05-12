from typing import Protocol
from processing_core.models import Conversion


class GetMyConversionsPort(Protocol):
    async def __call__(self, subject_id: str) -> list[Conversion]: ...
