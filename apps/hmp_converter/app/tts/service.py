import base64
import httpx
import uuid
import subprocess
import json
from langdetect import detect
from hmp_core.crypto import crypto
from hmp_core.storage import ObjectStorageClient
from hmp_core.events import EventClient
from app.shared.config.env import get_env_settings

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

async def get_instructor_public_key(pseudonym: str) -> bytes:
    settings = get_env_settings()
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.manager_url}/users/{pseudonym}/public-key")
        response.raise_for_status()
        data = response.json()
        return base64.b64decode(data["public_key"])

async def get_worker_private_key() -> bytes:
    # Mock for development:
    return b"dummy-worker-private-key-32bytes!!" # Must be 32 bytes for X25519

async def process_conversion(
    job_id: uuid.UUID,
    recipient_pseudonym: str,
    input_path: str,
    speed: int,
    storage: ObjectStorageClient,
    event_client: EventClient
):
    # 1. Download
    encrypted_pdf = await storage.download_file("hmp-processing", input_path)

    # 2. Decrypt (In-Memory)
    worker_sk = await get_worker_private_key()
    try:
        pdf_bytes = crypto.unseal(encrypted_pdf, private_key_bytes=worker_sk)
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

    # 3. Parse PDF
    from app.parser.service import extract_text_from_pdf
    text = extract_text_from_pdf(pdf_bytes)

    # 4. TTS
    audio_bytes = convert_text_to_audio(text, speed=speed)

    # 5. Encrypt for Instructor
    instructor_pk = await get_instructor_public_key(recipient_pseudonym)
    encrypted_audio = crypto.seal(audio_bytes, public_key_bytes=instructor_pk)

    # 6. Upload
    output_path = f"results/{recipient_pseudonym}/{job_id}.mp3.enc"
    await storage.ensure_bucket("hmp-results")
    await storage.upload_file("hmp-results", output_path, encrypted_audio)

    # 7. Notify Manager
    status_message = {
        "conversion_uuid": str(job_id),
        "output_path": output_path,
        "status": "completed",
        "metadata": {
            "size_bytes": len(audio_bytes),
            "duration_seconds": 0 
        }
    }
    
    await event_client.declare_exchange("hmp.jobs.results")
    await event_client.publish(
        routing_key="job.result.success",
        payload=json.dumps(status_message).encode(),
        correlation_id=str(job_id)
    )
