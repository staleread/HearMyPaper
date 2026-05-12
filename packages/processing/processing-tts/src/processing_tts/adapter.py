import asyncio
import subprocess
from typing import override
from langdetect import detect
from processing_core.ports.outgoing.tts import TTSPort


class ESpeakTTSAdapter(TTSPort):
    def __init__(self, default_speed: int = 140):
        self._default_speed = default_speed

    @override
    async def text_to_speech(self, text: str) -> bytes:
        lang = self._detect_language(text)
        voice = self._espeak_voice_for_lang(lang)

        # Use asyncio.create_subprocess_exec for non-blocking execution
        cmd = [
            "nice",
            "-n",
            "10",
            "espeak-ng",
            "--stdout",
            "-v",
            voice,
            "-s",
            str(self._default_speed),
            text,
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)

        if process.returncode != 0:
            raise RuntimeError(f"espeak-ng failed: {stderr.decode()}")

        return stdout

    def _detect_language(self, text: str) -> str:
        try:
            if not text or len(text.strip()) < 10:
                return "en"
            return str(detect(text))
        except Exception:
            return "en"

    def _espeak_voice_for_lang(self, lang: str) -> str:
        if lang == "uk":
            return "uk"
        return "en-us"
