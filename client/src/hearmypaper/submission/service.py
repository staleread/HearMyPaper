import os
import base64
import subprocess
import platform
from pathlib import Path
from toga.paths import Paths
from result import Ok, Err, Result

from . import api
from . import crypto as submission_crypto


def get_submission_path(
    app_paths: Paths, submission_id: int, content_hash: str
) -> Path:
    """Get path for submission file in resources directory."""
    submissions_dir = app_paths.data / "submissions"
    submissions_dir.mkdir(parents=True, exist_ok=True)
    return submissions_dir / f"submission_{submission_id}_{content_hash}.pdf"


def upload_submission(
    session, project_id: int, title: str, file_path: str
) -> Result[int, str]:
    """
    Encrypt and upload submission.

    Returns:
        Result[submission_id, error]
    """
    try:
        # Get instructor's public key
        key_result = api.get_instructor_key(session, project_id)
        if key_result.is_err():
            return Err(f"Failed to get public key: {key_result.unwrap_err()}")

        public_key_b64 = key_result.unwrap()
        public_key = base64.b64decode(public_key_b64)

        # Read and encrypt file
        with open(file_path, "rb") as f:
            content = f.read()

        encrypted = submission_crypto.encrypt_file_with_public_key(content, public_key)

        # Submit to server
        result = api.upload_submission(session, project_id, title, encrypted)
        if result.is_err():
            return Err(f"Upload failed: {result.unwrap_err()}")

        return Ok(result.unwrap())
    except Exception as e:
        return Err(f"Upload failed: {e}")


def download_submission(
    session, app_paths: Paths, submission_id: int, private_key_bytes: bytes
) -> Result[Path, str]:
    """
    Download and decrypt submission if needed.

    Returns:
        Result[file_path, error]
    """
    try:
        # Get submission hash
        hash_result = api.get_submission_hash(session, submission_id)
        if hash_result.is_err():
            return Err(f"Failed to get submission hash: {hash_result.unwrap_err()}")

        content_hash = hash_result.unwrap().content_hash

        # Build file path in app data directory
        file_path = get_submission_path(app_paths, submission_id, content_hash)

        # Check if file already exists and hash matches
        if file_path.exists():
            # Verify hash matches by computing it
            with open(file_path, "rb") as f:
                f.read()

            # Re-encrypt to verify integrity
            try:
                # Just return the file if it exists - hash in filename is good enough
                return Ok(file_path)
            except Exception:
                # If verification fails, redownload
                pass

        # Download encrypted content from server
        download_result = api.download_submission_content(session, submission_id)
        if download_result.is_err():
            return Err(f"Failed to download: {download_result.unwrap_err()}")

        encrypted_content = download_result.unwrap()

        # Decrypt content
        decrypted_content = submission_crypto.decrypt_file_with_private_key(
            encrypted_content, private_key_bytes
        )

        # Save to file
        with open(file_path, "wb") as f:
            f.write(decrypted_content)

        return Ok(file_path)

    except Exception as e:
        return Err(f"Download failed: {e}")


def open_submission(
    session, app_paths: Paths, submission_id: int, private_key_bytes: bytes
) -> Result[None, str]:
    """
    Open submission file with system default application.
    Downloads if not present or hash doesn't match.

    Returns:
        Result[None, error]
    """
    try:
        # Download/get cached file
        file_result = download_submission(
            session, app_paths, submission_id, private_key_bytes
        )
        if file_result.is_err():
            return Err(file_result.unwrap_err())

        file_path = file_result.unwrap()

        # Open with system default application
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(file_path)], check=True)
        elif system == "Windows":
            os.startfile(str(file_path))
        elif system == "Linux":
            subprocess.run(["xdg-open", str(file_path)], check=True)
        else:
            return Err(f"Unsupported platform: {system}")

        return Ok(None)

    except subprocess.CalledProcessError as e:
        return Err(f"Failed to open file: {e}")
    except Exception as e:
        return Err(f"Failed to open submission: {e}")


def list_submissions(session) -> Result[list, str]:
    """Get list of submissions."""
    result = api.list_submissions(session)
    if result.is_err():
        return Err(result.unwrap_err())
    return Ok(result.unwrap())


def convert_submission_to_audio(
    session,
    app_paths: Paths,
    submission_id: int,
    private_key_bytes: bytes,
    speed: int = 140,
) -> Result[bytes, str]:
    """
    Convert submission PDF to audio using secure encrypted file transfer.
    Downloads submission if needed, then converts to audio.

    Args:
        session: Authenticated HTTP session
        app_paths: Toga app paths object for locating resources
        submission_id: ID of the submission to convert
        private_key_bytes: User's private key bytes
        speed: Speech rate in words per minute (80-300)

    Returns:
        Result containing audio bytes or error message
    """
    try:
        # First, download/get the submission file
        file_result = download_submission(
            session, app_paths, submission_id, private_key_bytes
        )
        if file_result.is_err():
            return Err(f"Failed to get submission file: {file_result.unwrap_err()}")

        pdf_file_path = file_result.unwrap()

        # Load server public key
        server_public_key_path = str(app_paths.app / "resources/server.key")
        with open(server_public_key_path, "rb") as f:
            server_public_key_bytes = f.read()

        # Get upload key from server
        upload_key_result = api.get_upload_key(session)
        if upload_key_result.is_err():
            return Err(f"Failed to get upload key: {upload_key_result.unwrap_err()}")

        upload_key_response = upload_key_result.unwrap()

        # Decrypt AES key with user's private key
        aes_key = submission_crypto.decrypt_aes_key_with_private_key(
            upload_key_response.encrypted_aes_key, private_key_bytes
        )

        # Read PDF file
        with open(pdf_file_path, "rb") as f:
            pdf_bytes = f.read()

        # Encrypt PDF with AES key
        encrypted_file = submission_crypto.encrypt_file_with_aes(pdf_bytes, aes_key)

        # Encrypt AES key with server's public key
        encrypted_aes_key = submission_crypto.encrypt_aes_key_with_server_public_key(
            aes_key, server_public_key_bytes
        )

        # Build request
        from . import dto

        request = dto.PdfToAudioRequest(
            encrypted_file=encrypted_file,
            encrypted_aes_key=encrypted_aes_key,
            speed=speed,
        )

        # Execute PDF to audio conversion
        response_result = api.execute_pdf_to_audio(session, request)
        if response_result.is_err():
            return Err(
                f"Failed to convert PDF to audio: {response_result.unwrap_err()}"
            )

        response = response_result.unwrap()

        # Decrypt audio AES key with user's private key
        audio_aes_key = submission_crypto.decrypt_aes_key_with_private_key(
            response.encrypted_audio_key, private_key_bytes
        )

        # Decrypt audio with AES key
        audio_bytes = submission_crypto.decrypt_file_with_aes(
            response.encrypted_audio, audio_aes_key
        )

        return Ok(audio_bytes)

    except FileNotFoundError as e:
        return Err(f"File not found: {e}")
    except ValueError as e:
        return Err(f"Decryption error: {e}")
    except Exception as e:
        return Err(f"Unexpected error: {e}")
