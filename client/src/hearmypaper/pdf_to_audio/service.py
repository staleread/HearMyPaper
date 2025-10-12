import requests
from result import Result, Err, Ok
from toga.paths import Paths

from . import api
from .dto import PdfToAudioRequest
from .crypto import (
    decrypt_aes_key_with_private_key,
    encrypt_file_with_aes,
    decrypt_file_with_aes,
    encrypt_aes_key_with_server_public_key,
)
from ..auth.utils import get_user_credentials


def convert_pdf_to_audio(
    session: requests.Session,
    pdf_file_path: str,
    token_path: str,
    token_password: str,
    app_paths: Paths,
) -> Result[bytes, str]:
    """
    Convert PDF to audio using secure encrypted file transfer.

    Args:
        session: Authenticated HTTP session
        pdf_file_path: Path to the PDF file to convert
        token_path: Path to user's encrypted credentials file
        token_password: Password to decrypt user credentials
        app_paths: Toga app paths object for locating resources

    Returns:
        Result containing audio bytes or error message
    """
    try:
        # Load user's private key
        _, user_private_key_bytes = get_user_credentials(token_path, token_password)

        # Load server's public key from resources
        server_public_key_path = str(app_paths.app / "resources/server.key")
        with open(server_public_key_path, "rb") as f:
            server_public_key_bytes = f.read()

        # Step 1: Get upload key from server
        upload_key_result = api.get_upload_key(session)
        if upload_key_result.is_err():
            return Err(f"Failed to get upload key: {upload_key_result.unwrap_err()}")

        upload_key_response = upload_key_result.unwrap()

        # Step 2: Decrypt the AES key using user's private key
        aes_key = decrypt_aes_key_with_private_key(
            upload_key_response.encrypted_aes_key, user_private_key_bytes
        )

        # Step 3: Read and encrypt PDF file
        with open(pdf_file_path, "rb") as f:
            pdf_bytes = f.read()

        encrypted_file = encrypt_file_with_aes(pdf_bytes, aes_key)

        # Step 4: Encrypt AES key with server's public key
        encrypted_aes_key = encrypt_aes_key_with_server_public_key(
            aes_key, server_public_key_bytes
        )

        # Step 5: Send encrypted PDF to server
        request = PdfToAudioRequest(
            encrypted_file=encrypted_file, encrypted_aes_key=encrypted_aes_key
        )

        response_result = api.execute_pdf_to_audio(session, request)
        if response_result.is_err():
            return Err(
                f"Failed to convert PDF to audio: {response_result.unwrap_err()}"
            )

        response = response_result.unwrap()

        # Step 6: Decrypt audio AES key with user's private key
        audio_aes_key = decrypt_aes_key_with_private_key(
            response.encrypted_audio_key, user_private_key_bytes
        )

        # Step 7: Decrypt audio file
        audio_bytes = decrypt_file_with_aes(response.encrypted_audio, audio_aes_key)

        return Ok(audio_bytes)

    except FileNotFoundError as e:
        return Err(f"File not found: {e}")
    except ValueError as e:
        return Err(f"Decryption error: {e}")
    except Exception as e:
        return Err(f"Unexpected error: {e}")
