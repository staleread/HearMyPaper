import base64
from fastapi import APIRouter, HTTPException
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize
from app.audit.decorators import audit
from app.shared.config.env import env_settings
from app.shared.utils.crypto import (
    load_server_private_key,
    generate_aes_key,
    encrypt_with_aes,
    decrypt_with_aes,
    encrypt_with_ed25519_public_key,
    decrypt_with_ed25519_private_key,
)

from .dto import UploadKeyResponse, PdfToAudioRequest, PdfToAudioResponse
from . import service as pdf_service

router = APIRouter()

# Load server private key on module initialization
SERVER_PRIVATE_KEY: Ed25519PrivateKey | None = None
try:
    SERVER_PRIVATE_KEY = load_server_private_key(
        env_settings.server_private_key_password
    )
except Exception as e:
    print(f"Warning: Could not load server private key: {e}")


@router.get("/upload-key")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def read_upload_key(
    db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> UploadKeyResponse:
    """
    Generate an AES key, encrypt it with user's public key, and return it.
    The client will use this key to encrypt the PDF file.
    """
    if not SERVER_PRIVATE_KEY:
        raise HTTPException(status_code=500, detail="Server private key not configured")

    # Get user's public key from database
    user_public_key_row = (
        db.query("""
        SELECT public_key
        FROM users
        WHERE id = :user_id
    """)
        .bind(user_id=subject.id)
        .first_row()
    )

    if not user_public_key_row or not user_public_key_row["public_key"]:
        raise HTTPException(
            status_code=400, detail="User public key not found in database"
        )

    user_public_key_bytes = bytes(user_public_key_row["public_key"])

    # Generate AES key (32 bytes for AES-256)
    aes_key = generate_aes_key()

    # Encrypt AES key with user's public key
    encrypted_aes_key = encrypt_with_ed25519_public_key(aes_key, user_public_key_bytes)

    return UploadKeyResponse(
        encrypted_aes_key=base64.b64encode(encrypted_aes_key).decode("utf-8")
    )


@router.post("/execute")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def execute_pdf_to_audio(
    req: PdfToAudioRequest, db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> PdfToAudioResponse:
    """
    Receive encrypted PDF, decrypt it, convert to audio, encrypt audio, and return.

    Process:
    1. Decrypt the AES key using server's private key
    2. Decrypt the PDF file using the AES key
    3. Extract text from PDF
    4. Convert text to audio
    5. Generate new AES key for audio
    6. Encrypt audio with new key
    7. Encrypt the new key with user's public key
    8. Return encrypted audio and encrypted key
    """
    if not SERVER_PRIVATE_KEY:
        raise HTTPException(status_code=500, detail="Server private key not configured")

    try:
        # Decode from base64
        encrypted_file_bytes = base64.b64decode(req.encrypted_file)
        encrypted_aes_key_bytes = base64.b64decode(req.encrypted_aes_key)

        # Decrypt AES key using server's private key
        aes_key = decrypt_with_ed25519_private_key(
            encrypted_aes_key_bytes, SERVER_PRIVATE_KEY
        )

        # Decrypt PDF file
        pdf_bytes = decrypt_with_aes(encrypted_file_bytes, aes_key)

        # Extract text from PDF
        text = pdf_service.extract_text_from_pdf(pdf_bytes)

        if not text.strip():
            raise HTTPException(
                status_code=400, detail="No text found in PDF or PDF is empty"
            )

        # Convert text to audio
        audio_bytes = pdf_service.convert_text_to_audio(text, speed=req.speed)

        # Generate new AES key for audio encryption
        audio_aes_key = generate_aes_key()

        # Encrypt audio with new AES key
        encrypted_audio = encrypt_with_aes(audio_bytes, audio_aes_key)

        # Get user's public key for encrypting the audio AES key
        user_public_key_row = (
            db.query("""
            SELECT public_key
            FROM users
            WHERE id = :user_id
        """)
            .bind(user_id=subject.id)
            .first_row()
        )

        if not user_public_key_row or not user_public_key_row["public_key"]:
            raise HTTPException(
                status_code=400, detail="User public key not found in database"
            )

        user_public_key_bytes = bytes(user_public_key_row["public_key"])

        # Encrypt audio AES key with user's public key
        encrypted_audio_aes_key = encrypt_with_ed25519_public_key(
            audio_aes_key, user_public_key_bytes
        )

        return PdfToAudioResponse(
            encrypted_audio=base64.b64encode(encrypted_audio).decode("utf-8"),
            encrypted_audio_key=base64.b64encode(encrypted_audio_aes_key).decode(
                "utf-8"
            ),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Decryption error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"PDF to audio conversion failed: {str(e)}"
        )
