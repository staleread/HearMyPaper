from typing import Protocol


class ParserPort(Protocol):
    async def extract_text(self, pdf_bytes: bytes) -> str: ...
