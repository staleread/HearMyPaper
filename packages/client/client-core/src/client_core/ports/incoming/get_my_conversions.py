from typing import Protocol
from ...models import Conversion


class GetMyConversionsPort(Protocol):
    async def __call__(self) -> list[Conversion]: ...
