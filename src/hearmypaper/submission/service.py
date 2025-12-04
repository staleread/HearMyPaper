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
    try:
        key_result = api.get_instructor_key(session, project_id)
        if key_result.is_err():
            return Err(f"Failed to get public key: {key_result.unwrap_err()}")

        public_key_b64 = key_result.unwrap()
        public_key = base64.b64decode(public_key_b64)

        with open(file_path, "rb") as f:
            content = f.read()

        encrypted = submission_crypto.encrypt_file_with_public_key(content, public_key)

        result = api.upload_submission(session, project_id, title, encrypted)
        if result.is_err():
            return Err(f"Upload failed: {result.unwrap_err()}")

        return Ok(result.unwrap())
    except Exception as e:
        return Err(f"Upload failed: {e}")


def download_submission(
    session, app_paths: Paths, submission_id: int, private_key_bytes: bytes
) -> Result[Path, str]:
    try:
        hash_result = api.get_submission_hash(session, submission_id)
        if hash_result.is_err():
            return Err(f"Failed to get submission hash: {hash_result.unwrap_err()}")

        content_hash = hash_result.unwrap().content_hash
        file_path = get_submission_path(app_paths, submission_id, content_hash)

        if file_path.exists():
            return Ok(file_path)

        download_result = api.download_submission_content(session, submission_id)
        if download_result.is_err():
            return Err(f"Failed to download: {download_result.unwrap_err()}")

        encrypted_content = download_result.unwrap()

        decrypted_content = submission_crypto.decrypt_file_with_private_key(
            encrypted_content, private_key_bytes
        )

        with open(file_path, "wb") as f:
            f.write(decrypted_content)

        return Ok(file_path)

    except Exception as e:
        return Err(f"Download failed: {e}")


def open_submission(
    session, app_paths: Paths, submission_id: int, private_key_bytes: bytes
) -> Result[None, str]:
    try:
        file_result = download_submission(
            session, app_paths, submission_id, private_key_bytes
        )
        if file_result.is_err():
            return Err(file_result.unwrap_err())

        file_path = file_result.unwrap()

        system = platform.system()
        if system == "Darwin":
            subprocess.run(["open", str(file_path)], check=True)
        elif system == "Windows":
            import os

            if hasattr(os, "startfile"):
                os.startfile(str(file_path))  # type: ignore
            else:
                subprocess.run(["cmd", "/c", "start", str(file_path)], check=True)
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
    Convert submission PDF to audio using secure encrypted file transfer with polling.

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

        with open(pdf_file_path, "rb") as f:
            pdf_bytes = f.read()

        task_uuid = None
        aes_key = None
        encrypted_file = None

        import time

        max_upload_key_attempts = 60
        for attempt in range(max_upload_key_attempts):
            print(
                f"[DEBUG CLIENT] Upload key attempt {attempt + 1}/{max_upload_key_attempts}"
            )
            upload_key_result = api.get_upload_key(session)
            if upload_key_result.is_err():
                return Err(
                    f"Failed to get upload key: {upload_key_result.unwrap_err()}"
                )

            upload_key_response = upload_key_result.unwrap()
            print(
                f"[DEBUG CLIENT] Upload key response: is_success={upload_key_response.is_success}"
            )

            if upload_key_response.is_success:
                if (
                    upload_key_response.encrypted_aes_key is not None
                    and upload_key_response.task_uuid is not None
                ):
                    aes_key = submission_crypto.decrypt_aes_key_with_private_key(
                        base64.b64decode(upload_key_response.encrypted_aes_key),
                        private_key_bytes,
                    )
                    task_uuid = upload_key_response.task_uuid
                    encrypted_file = submission_crypto.encrypt_file_with_aes(
                        pdf_bytes, aes_key
                    )
                    print(f"[DEBUG CLIENT] Got upload key, task_uuid={task_uuid}")
                    break

            if attempt < max_upload_key_attempts - 1:
                time.sleep(5)

        if task_uuid is None or encrypted_file is None:
            return Err("Failed to obtain upload key: converter busy for too long")

        from . import dto

        request = dto.PdfToAudioRequest(
            encrypted_file=encrypted_file,
            speed=speed,
        )

        max_trigger_attempts = 60
        for attempt in range(max_trigger_attempts):
            print(
                f"[DEBUG CLIENT] Execute attempt {attempt + 1}/{max_trigger_attempts}"
            )
            response_result = api.execute_pdf_to_audio(session, request, task_uuid)
            if response_result.is_err():
                return Err(
                    f"Failed to trigger conversion: {response_result.unwrap_err()}"
                )

            response = response_result.unwrap()
            print(f"[DEBUG CLIENT] Execute response: is_success={response.is_success}")
            if response.is_success:
                print("[DEBUG CLIENT] Conversion triggered successfully")
                break

            if attempt < max_trigger_attempts - 1:
                time.sleep(5)
        else:
            return Err("Failed to trigger conversion: converter busy for too long")

        print("[DEBUG CLIENT] Starting status polling...")
        max_status_attempts = 120
        for attempt in range(max_status_attempts):
            print(
                f"[DEBUG CLIENT] Status check attempt {attempt + 1}/{max_status_attempts}"
            )
            status_result = api.get_conversion_status(session, task_uuid)
            if status_result.is_err():
                print(
                    f"[DEBUG CLIENT] Status check failed: {status_result.unwrap_err()}"
                )
                return Err(
                    f"Failed to get conversion status: {status_result.unwrap_err()}"
                )

            status = status_result.unwrap()
            print(
                f"[DEBUG CLIENT] Status: is_done={status.is_done}, has_error={status.has_error}, error_message={status.error_message}"
            )

            if status.has_error:
                print("[DEBUG CLIENT] Conversion has error, exiting loop")
                return Err(f"Conversion failed: {status.error_message}")

            if status.is_done:
                print("[DEBUG CLIENT] Conversion is done, exiting loop")
                break

            if attempt < max_status_attempts - 1:
                print("[DEBUG CLIENT] Not done yet, sleeping 5 seconds...")
                time.sleep(5)
        else:
            print(f"[DEBUG CLIENT] Timeout after {max_status_attempts} attempts")
            return Err("Conversion timed out: took too long to complete")

        audio_result = api.get_converted_audio(session, task_uuid)
        if audio_result.is_err():
            return Err(f"Failed to download audio: {audio_result.unwrap_err()}")

        audio_response = audio_result.unwrap()

        audio_aes_key = submission_crypto.decrypt_aes_key_with_private_key(
            audio_response.encrypted_audio_key, private_key_bytes
        )

        audio_bytes = submission_crypto.decrypt_file_with_aes(
            audio_response.encrypted_audio, audio_aes_key
        )

        return Ok(audio_bytes)

    except FileNotFoundError as e:
        return Err(f"File not found: {e}")
    except ValueError as e:
        return Err(f"Decryption error: {e}")
    except Exception as e:
        return Err(f"Unexpected error: {e}")
