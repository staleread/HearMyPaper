import toga
import requests
from toga.paths import Paths
from typing import Any
from collections.abc import Callable


class Navigator:
    def __init__(self, main_window: toga.MainWindow, app_paths: Paths):
        self.main_window = main_window
        self.screens: dict[str, Callable[[Any], toga.Widget]] = {}
        self.data_screens: dict[str, Callable[..., toga.Widget]] = {}

        self.session = requests.Session()
        self.session.verify = str(app_paths.app / "resources/server.crt")

    def register_screen(self, name: str, screen_factory: Callable[[Any], toga.Widget]):
        self.screens[name] = screen_factory

    def register_data_screen(
        self, name: str, screen_factory: Callable[..., toga.Widget]
    ):
        self.data_screens[name] = screen_factory

    def navigate(self, name: str):
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not registered")

        widget = self.screens[name](self)
        self.main_window.content = widget

    def navigate_with_data(self, name: str, *args: Any, **kwargs: Any):
        if name not in self.data_screens:
            raise ValueError(f"Data screen '{name}' not registered")

        widget = self.data_screens[name](self, *args, **kwargs)
        self.main_window.content = widget
