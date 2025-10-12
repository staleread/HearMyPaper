import tempfile
import fitz  # type: ignore
import pyttsx3  # type: ignore


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyMuPDF."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def convert_text_to_audio(text: str) -> bytes:
    """Convert text to audio using pyttsx3 and return as bytes."""
    engine = pyttsx3.init()

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        engine.save_to_file(text, temp_path)
        engine.runAndWait()

        with open(temp_path, "rb") as f:
            audio_bytes = f.read()

        return audio_bytes
    finally:
        import os

        if os.path.exists(temp_path):
            os.remove(temp_path)
