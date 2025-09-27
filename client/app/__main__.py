import sys
from PyQt5.QtWidgets import QApplication

from app.utils.navigator import Navigator
from app.services.auth_service import register, login


class AuthService:
    def register(self, username, role, token_path, password):
        return register(username, role, token_path, password)

    def login(self, token_path, password):
        return login(token_path, password)


class MainApp:
    def __init__(self):
        self.auth_service = AuthService()
        self.main_window = Navigator(self.auth_service)

    def show_login(self):
        self.main_window.show_login()
        self.main_window.show()

    def register(self, username, role, token_path, password):
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    navigator = Navigator(AuthService())
    navigator.show()
    app.exec()
