from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from app.ui.login_screen import LoginScreen
from app.ui.register_screen import RegisterScreen
from app.ui.user_profile_screen import UserProfileScreen
from app.ui.submition_screen import SubmissionsListScreen


class Navigator(QMainWindow):
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.screens = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("HearMyPaper")
        self.setGeometry(100, 100, 600, 500)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.register_screen(
            "login", lambda: LoginScreen(self.auth_service, navigator=self)
        )
        self.register_screen(
            "register", lambda: RegisterScreen(self.auth_service, navigator=self)
        )

        self.screens["login"].navigate_to_register.connect(
            lambda: self.navigate("register")
        )
        self.screens["register"].navigate_to_login.connect(
            lambda: self.navigate("login")
        )

        self.navigate("login")

    def register_screen(self, name, screen_factory):
        screen = screen_factory()
        self.screens[name] = screen
        self.stacked_widget.addWidget(screen)

    def navigate(self, name):
        if name in self.screens:
            self.stacked_widget.setCurrentWidget(self.screens[name])
        else:
            raise ValueError(f"Screen '{name}' not registered")

    def navigate_user_profile(self, user_data):
        profile_screen = UserProfileScreen(
            user_data, navigator=self
        )  # <- передаємо navigator
        self.stacked_widget.addWidget(profile_screen)
        self.stacked_widget.setCurrentWidget(profile_screen)

    def navigate_submissions(self, user_role, projects):
        submissions_screen = SubmissionsListScreen(user_role, projects)
        self.stacked_widget.addWidget(submissions_screen)
        self.stacked_widget.setCurrentWidget(submissions_screen)
