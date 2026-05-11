import toml
import toga
import httpx
from toga.paths import Paths
from typing import Callable, Any

from client_core.ports.outgoing.session import SessionProviderPort
from client_server_bridge import (
    IdentityPortAdapter,
    EducationPortAdapter,
    SubmissionsPortAdapter,
)
from client_credentials import FileCredentialsStorageAdapter
from client_core.use_cases.login import LoginUseCase
from client_core.use_cases.get_user import GetUserUseCase
from client_core.use_cases.create_user import CreateUserUseCase
from client_core.use_cases.update_user import UpdateUserUseCase
from client_core.use_cases.get_project import GetProjectUseCase
from client_core.use_cases.create_project import CreateProjectUseCase
from client_core.use_cases.update_project import UpdateProjectUseCase
from client_core.use_cases.get_project_attempts import GetProjectAttemptsUseCase
from client_core.use_cases.get_attempt import GetAttemptUseCase
from client_core.use_cases.grade_attempt import GradeAttemptUseCase
from client_core.use_cases.get_my_projects import GetMyProjectsUseCase
from client_core.use_cases.manage_students import ManageStudentsUseCase
from client_core.use_cases.upload_submission import UploadSubmissionUseCase
from client_core.use_cases.download_attempt import DownloadAttemptUseCase
from client_file_manager import HttpFileManagerAdapter
from client_crypto import CryptoAdapter


class SessionProvider(SessionProviderPort):
    def __init__(self, async_client: httpx.AsyncClient):
        self._token: str | None = None
        self._async_client = async_client

    def get_token(self) -> str | None:
        return self._token

    def set_token(self, token: str) -> None:
        self._token = token
        self._async_client.headers["authorization"] = f"Bearer {token}"


class Navigator:
    def __init__(self, main_window: toga.MainWindow, app_paths: Paths):
        self.main_window = main_window
        self.app_paths = app_paths
        self.screens: dict[str, Callable[[Any], toga.Widget]] = {}

        # Load config from resources
        config_path = app_paths.app / "resources/config.toml"
        with open(config_path, "r") as f:
            config = toml.load(f)

        self.api_base_url = config.get("api", {}).get(
            "base_url", "http://localhost:8000"
        )
        self.download_path = config.get("storage", {}).get(
            "download_path", "~/Downloads/HearMyPaper"
        )
        self.async_client = httpx.AsyncClient(base_url=self.api_base_url)

        # Adapters
        self.session_provider = SessionProvider(self.async_client)
        self.identity_port = IdentityPortAdapter(self.async_client)
        self.education_port = EducationPortAdapter(self.async_client)
        self.submissions_port = SubmissionsPortAdapter(self.async_client)
        self.credentials_port = FileCredentialsStorageAdapter()
        self.file_manager_port = HttpFileManagerAdapter()
        self.crypto_port = CryptoAdapter()

        # Use Cases
        self.login_use_case = LoginUseCase(
            identity=self.identity_port,
            credentials=self.credentials_port,
            session_provider=self.session_provider,
            crypto=self.crypto_port,
        )
        self.get_user_use_case = GetUserUseCase(identity=self.identity_port)
        self.create_user_use_case = CreateUserUseCase(
            identity=self.identity_port,
            credentials=self.credentials_port,
            crypto=self.crypto_port,
        )
        self.update_user_use_case = UpdateUserUseCase(identity=self.identity_port)
        self.get_project_use_case = GetProjectUseCase(education=self.education_port)
        self.create_project_use_case = CreateProjectUseCase(
            education=self.education_port
        )
        self.update_project_use_case = UpdateProjectUseCase(
            education=self.education_port
        )
        self.get_project_attempts_use_case = GetProjectAttemptsUseCase(
            education=self.education_port
        )
        self.get_attempt_use_case = GetAttemptUseCase(education=self.education_port)
        self.grade_attempt_use_case = GradeAttemptUseCase(education=self.education_port)
        self.get_my_projects_use_case = GetMyProjectsUseCase(
            education=self.education_port
        )
        self.manage_students_use_case = ManageStudentsUseCase(
            education=self.education_port
        )
        self.upload_submission_use_case = UploadSubmissionUseCase(
            submissions=self.submissions_port,
            file_manager=self.file_manager_port,
        )
        self.download_attempt_use_case = DownloadAttemptUseCase(
            education=self.education_port,
            file_manager=self.file_manager_port,
        )

        self.credentials_path: str | None = None

    def register_screen(self, name, screen_factory):
        self.screens[name] = screen_factory

    def navigate(self, name, *args, **kwargs):
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not registered")

        widget = self.screens[name](self, *args, **kwargs)
        self.main_window.content = widget
