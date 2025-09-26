from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from datetime import datetime
from dateutil import parser


class UserProfileScreen(QWidget):
    def __init__(self, user_data: dict):
        """
        user_data: {
            "username": str,
            "registered_at": str,  # ISO 8601 string
            "last_login_at": str    # ISO 8601 string
        }
        """
        super().__init__()
        self.user_data = user_data
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


        title_label = QLabel(f"Welcome, {self.user_data.get('username', 'User')}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #3F51B5;
        """)
        container_layout.addWidget(title_label)


        registered_at = parser.isoparse(self.user_data.get("registered_at"))
        reg_label = QLabel(f"Registered at: {registered_at.strftime('%Y-%m-%d %H:%M:%S %z')}")
        reg_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(reg_label)


        last_login_at = parser.isoparse(self.user_data.get("last_login_at"))
        login_label = QLabel(f"Last login: {last_login_at.strftime('%Y-%m-%d %H:%M:%S %z')}")
        login_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(login_label)

        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

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
