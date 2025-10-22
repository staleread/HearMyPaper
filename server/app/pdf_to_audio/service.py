from io import BytesIO
import fitz  # type: ignore
from gtts import gTTS  # type: ignore
from langdetect import detect  # type: ignore


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyMuPDF."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def convert_text_to_audio(text: str) -> bytes:
    """
    Convert text to audio using Google Text-to-Speech.
    Automatically detects language and supports Ukrainian.
    Returns audio data directly from memory buffer.
    """
    # Detect language from text
    try:
        lang = detect(text)
        # Map to gTTS supported codes
        if lang not in ["uk", "en", "ru", "de", "fr", "es", "it", "pl", "ja", "zh-cn"]:
            lang = "en"  # Default to English if unsupported
    except Exception:
        lang = "uk"  # Default to Ukrainian if detection fails

    # Create TTS object
    tts = gTTS(text=text, lang=lang, slow=False)

    # Write directly to BytesIO buffer
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)

    # Get bytes from buffer
    audio_buffer.seek(0)
    return audio_buffer.read()
