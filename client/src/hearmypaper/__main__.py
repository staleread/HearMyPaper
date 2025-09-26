import sys
import os
from PyQt5.QtWidgets import QApplication


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from utils.navigator import Navigator
from services.auth_service import register, login

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


class DummyAuth:
    def login(self, token_path, password):
        if token_path.endswith(".txt") and password == "1234":
            return None
        return "Invalid credentials"

    def register(self, username, role, token_path, password):
        return None

def main():
    app = QApplication(sys.argv)
    auth_service = DummyAuth()
    navigator = Navigator(auth_service)
    navigator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
