from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt
from dateutil import parser

class UserProfileScreen(QWidget):
    def __init__(self, user_data: dict, navigator=None):
        """
        user_data: dict з інформацією про користувача
        navigator: екземпляр Navigator, щоб повертатися на login_screen
        """
        super().__init__()
        self.user_data = user_data
        self.navigator = navigator
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Profile")
        self.setMinimumSize(400, 500)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        container = QFrame()
        container.setMaximumWidth(400)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(15)
        container_layout.setContentsMargins(0, 0, 0, 0)

        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Заголовок
        title_label = QLabel(f"Welcome, {self.user_data.get('username', 'User')}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size:28px; font-weight:700; color:#3F51B5;")
        container_layout.addWidget(title_label)

        # Дата реєстрації
        registered_at = parser.isoparse(self.user_data.get("registered_at"))
        reg_label = QLabel(f"Registered at: {registered_at.strftime('%Y-%m-%d %H:%M:%S %z')}")
        reg_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(reg_label)

        # Дата останнього логіну
        last_login_at = parser.isoparse(self.user_data.get("last_login_at"))
        login_label = QLabel(f"Last login: {last_login_at.strftime('%Y-%m-%d %H:%M:%S %z')}")
        login_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(login_label)

        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка назад
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3F51B5;
                color: white;
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #303F9F;
            }
        """)
        back_button.clicked.connect(self.go_back)
        container_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8EAF6, stop:1 #FFFFFF
                );
            }
        """)

    def go_back(self):
        """Повертає на login_screen через navigator"""
        if self.navigator:
            self.navigator.navigate("login")
