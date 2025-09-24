from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from .login_screen import LoginScreen
from .register_screen import RegisterScreen


class MainWindow(QMainWindow):
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("HearMyPaper")
        self.setGeometry(100, 100, 400, 500)

        # Створюємо stacked widget для навігації
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Створюємо екрани
        self.login_screen = LoginScreen(self.auth_service)
        self.register_screen = RegisterScreen(self.auth_service)

        # Додаємо екрани до stacked widget
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)

        # Підключаємо сигнали навігації
        self.login_screen.navigate_to_register.connect(self.show_register)
        self.register_screen.navigate_to_login.connect(self.show_login)

        # Показуємо екран логіну спочатку
        self.show_login()

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register_screen)