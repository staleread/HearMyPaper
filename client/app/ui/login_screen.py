from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import pyqtSignal, Qt
from datetime import datetime

from app.ui.dashboard_screen import DashboardScreen


class LoginScreen(QWidget):
    navigate_to_register = pyqtSignal()

    def __init__(self, auth_service, navigator=None):
        super().__init__()
        self.auth_service = auth_service
        self.navigator = navigator
        self.token_path = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setMinimumSize(420, 500)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(40, 40, 40, 40)

        content_container = QFrame()
        content_container.setFixedWidth(340)
        content_container.setMaximumWidth(340)
        content_container.setMaximumHeight(600)
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.title_label = QLabel("Welcome Back")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #3F51B5;
        """)
        content_layout.addWidget(self.title_label)

        self.token_button = QPushButton("Select Token File")
        self.token_button.clicked.connect(self.pick_file)
        self.token_button.setCursor(Qt.PointingHandCursor)
        self.token_button.setStyleSheet(self.button_style("#3F51B5"))
        content_layout.addWidget(self.token_button)

        self.token_label = QLabel("No file selected")
        self.token_label.setStyleSheet("color: #9E9E9E; font-size: 12px;")
        self.token_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.token_label)

        pw_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        pw_layout.addWidget(self.password_input)

        self.eye_button = QPushButton("👁")
        self.eye_button.setFixedWidth(35)
        self.eye_button.setCheckable(True)
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        self.eye_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 16px;
                color: #9E9E9E;
            }
            QPushButton:checked {
                color: #3F51B5;
            }
        """)
        pw_layout.addWidget(self.eye_button)
        content_layout.addLayout(pw_layout)

        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.setStyleSheet(self.gradient_button_style())
        content_layout.addWidget(self.submit_button)

        self.register_button = QPushButton("Create an account")
        self.register_button.clicked.connect(self.navigate_to_register.emit)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #3F51B5;
                border: none;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #303F9F;
            }
        """)
        content_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        content_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        main_layout.addWidget(content_container)
        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8EAF6, stop:1 #FFFFFF
                );
            }
        """)

    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.eye_button.setText("👁‍🗨")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.eye_button.setText("👁")

    def pick_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select token path", "", "All Files (*)"
        )
        if file_path:
            self.token_path = file_path
            self.token_label.setText(file_path)

    def on_submit(self):
        if not self.token_path or not self.password_input.text():
            QMessageBox.warning(self, "Error", "Token and password required")
            return

        error = self.auth_service.login(self.token_path, self.password_input.text())
        if not error:
            user_data = {
                "username": "TestUser",
                "registered_at": "2025-09-26T12:00:00+03:00",
                "last_login_at": datetime.now().isoformat(),
            }
            projects = [
                {
                    "title": "Math",
                    "syllabus": "Algebra",
                    "status": "Submitted",
                    "deadline": "2025-09-30",
                },
                {
                    "title": "Physics",
                    "syllabus": "Mechanics",
                    "status": "Pending",
                    "deadline": "2025-10-01",
                },
            ]
            if self.navigator:
                dashboard = DashboardScreen(
                    self.navigator, user_data, projects
                )  # ⬅️ новий код
                self.navigator.stacked_widget.addWidget(dashboard)  # ⬅️ новий код
                self.navigator.stacked_widget.setCurrentWidget(dashboard)  # ⬅️ новий код
        else:
            QMessageBox.critical(self, "Error", error)

    @staticmethod
    def button_style(color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #303F9F;
            }}
            QPushButton:pressed {{
                background-color: #1A237E;
            }}
        """

    @staticmethod
    def gradient_button_style():
        return """
            QPushButton {
                border-radius: 10px;
                padding: 12px;
                color: white;
                font-size: 14px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3F51B5, stop:1 #2196F3
                );
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #303F9F, stop:1 #03A9F4
                );
            }
            QPushButton:pressed {
                background-color: #1A237E;
            }
        """

    @staticmethod
    def input_style():
        return """
            QLineEdit {
                border-radius: 8px;
                padding: 10px;
                border: 2px solid #BDBDBD;
                background-color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3F51B5;
            }
        """
