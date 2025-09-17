import toga
from toga.style.pack import COLUMN, ROW

from .utils.navigator import Navigator
from .ui.login_screen import login_screen
from .ui.register_screen import register_screen


class HearMyPaper(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="HearMyPaper")
        self.navigator = Navigator(self.main_window)

        self.navigator.register_screen("login", login_screen)
        self.navigator.register_screen("register", register_screen)

        self.navigator.navigate("login")
        self.main_window.show()


def main():
    return HearMyPaper()
