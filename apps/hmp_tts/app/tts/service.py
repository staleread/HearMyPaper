import subprocess
from langdetect import detect

def _detect_language(text: str) -> str:
    try:
        if not text or len(text.strip()) < 10:
            return "en"
        lang = detect(text)
        return str(lang)
    except Exception:
        return "en"


def _espeak_voice_for_lang(lang: str) -> str:
    if lang == "uk":
        return "uk"
    return "en-us"


def convert_text_to_audio(text: str, speed: int = 140) -> bytes:
    lang = _detect_language(text)
    espeak_voice = _espeak_voice_for_lang(lang)

    cmd = [
        "nice",
        "-n",
        "10",
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
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=300,
        )
        return proc.stdout
    except subprocess.TimeoutExpired:
        raise ValueError("Text-to-speech conversion timed out")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Text-to-speech conversion failed: {e}")
