from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class DashboardScreen(QWidget):
    def __init__(self, navigator, user_data, projects=None):
        """
        navigator: екземпляр Navigator для переходів між екранами
        user_data: dict з інформацією про користувача
        projects: список проектів для SubmissionsListScreen
        """
        super().__init__()
        self.navigator = navigator
        self.user_data = user_data
        self.projects = projects or []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        profile_btn = QPushButton("Go to User Profile")
        profile_btn.setStyleSheet("background-color:#3F51B5; color:white; padding:12px; border-radius:8px; font-size:16px;")
        profile_btn.clicked.connect(self.go_to_profile)
        layout.addWidget(profile_btn)

        submissions_btn = QPushButton("Go to Submissions")
        submissions_btn.setStyleSheet("background-color:#2196F3; color:white; padding:12px; border-radius:8px; font-size:16px;")
        submissions_btn.clicked.connect(self.go_to_submissions)
        layout.addWidget(submissions_btn)

        self.setLayout(layout)

    def go_to_profile(self):
        self.navigator.navigate_user_profile(self.user_data)

    def go_to_submissions(self):
        self.navigator.navigate_submissions("Student", self.projects)  # або передати роль динамічно
