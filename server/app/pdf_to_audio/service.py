import subprocess
import fitz  # type: ignore
from langdetect import detect  # type: ignore


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_parts = []

    for page in doc:
        text_parts.append(page.get_text())
    doc.close()

    return "".join(text_parts)


def _detect_language(text: str) -> str:
    try:
        if not text or len(text.strip()) < 10:
            return "en"
        lang = detect(text)
        return lang
    except Exception:
        return "en"


def _espeak_voice_for_lang(lang: str) -> str:
    """Map detected lang to an espeak-ng voice code."""
    if lang == "uk":
        return "uk"  # Ukrainian

    return "en-us"


def convert_text_to_audio(text: str, speed: int = 140) -> bytes:
    """
    Convert text to audio bytes in WAV format.

    Uses espeak-ng --stdout to get WAV bytes in-memory.

    Parameters:
    - text: str - input text to synthesize
    - speed: speaking rate for espeak-ng (words per minute)

    Returns:
    - bytes of WAV audio
    """
    lang = _detect_language(text)
    espeak_voice = _espeak_voice_for_lang(lang)

    # espeak(-ng) writes RIFF WAV to stdout when --stdout is used
    cmd = [
        "espeak-ng",
        "--stdout",
        "-v",
        espeak_voice,
        "-s",
        str(speed),
        text,
    ]
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        wav_bytes = proc.stdout
        return wav_bytes
    except subprocess.CalledProcessError as e:
        print(
            f"espeak command failed: {e}; stderr: {e.stderr.decode(errors='ignore') if e.stderr else ''}"
        )
