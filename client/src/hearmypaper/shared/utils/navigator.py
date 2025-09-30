import toga
import requests
from typing import Any
from collections.abc import Callable


class Navigator:
    def __init__(self, main_window: toga.MainWindow):
        self.main_window = main_window
        self.screens: dict[str, Callable[[Any], toga.Widget]] = {}
        self.data_screens: dict[str, Callable[..., toga.Widget]] = {}

        # Initialize requests session with SSL certificate
        self.session = requests.Session()
        # TODO: replace with relative path
        self.session.verify = "/home/mykola/edu/chnu/python-web/HearMyPaper/server/nginx/hearmypaper.edu.crt"

    def register_screen(self, name: str, screen_factory: Callable[[Any], toga.Widget]):
        """Register a screen that takes only navigator as parameter"""
        self.screens[name] = screen_factory

    def register_data_screen(
        self, name: str, screen_factory: Callable[..., toga.Widget]
    ):
        """Register a screen that takes navigator and additional data parameters"""
        self.data_screens[name] = screen_factory

    def navigate(self, name: str):
        """Navigate to a screen without data"""
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not registered")

        widget = self.screens[name](self)
        self.main_window.content = widget

    def navigate_with_data(self, name: str, *args: Any, **kwargs: Any):
        """Navigate to a screen with data parameters"""
        if name not in self.data_screens:
            raise ValueError(f"Data screen '{name}' not registered")

        widget = self.data_screens[name](self, *args, **kwargs)
        self.main_window.content = widget
