import toga
from toga.paths import Paths
from typing import Callable, Any

from .session import ApiSession


class Navigator:
    def __init__(self, main_window: toga.MainWindow, app_paths: Paths):
        self.main_window = main_window
        self.app_paths = app_paths
        self.screens: dict[str, Callable[[Any], toga.Widget]] = {}
        self.session = ApiSession(base_url="https://localhost/")
        self.session.verify = str(app_paths.app / "resources/server.crt")
        self.credentials_path: str | None = None

    def register_screen(self, name, screen_factory):
        self.screens[name] = screen_factory

    def navigate(self, name, *args, **kwargs):
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not registered")

        widget = self.screens[name](self, *args, **kwargs)
        self.main_window.content = widget
