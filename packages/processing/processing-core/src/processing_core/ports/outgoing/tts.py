from typing import Protocol


class TTSPort(Protocol):
    async def text_to_speech(self, text: str) -> bytes: ...
