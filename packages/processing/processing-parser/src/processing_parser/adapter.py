import fitz
from typing import override
from processing_core.ports.outgoing.parser import ParserPort


class PyMuPDFParserAdapter(ParserPort):
    @override
    async def extract_text(self, pdf_bytes: bytes) -> str:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text_parts = []

        for page in doc:
            text_parts.append(page.get_text())
        doc.close()

        return "".join(text_parts)
