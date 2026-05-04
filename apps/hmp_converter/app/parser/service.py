import fitz


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_parts = []

    for page in doc:
        text_parts.append(page.get_text())
    doc.close()

    return "".join(text_parts)
