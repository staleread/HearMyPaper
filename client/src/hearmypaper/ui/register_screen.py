from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, Qt


class RegisterScreen(QWidget):
    navigate_to_login = pyqtSignal()

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.token_path = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register")
        self.setFixedSize(420, 520)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)

        # Title
        title_label = QLabel("Create Account")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #3F51B5;
        """)
        main_layout.addWidget(title_label)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(self.input_style())
        main_layout.addWidget(QLabel("Username:"))
        main_layout.addWidget(self.username_input)

        # Role selection
        main_layout.addWidget(QLabel("Role:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student", "Instructor"])
        self.role_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                border: 2px solid #BDBDBD;
                background-color: #FFFFFF;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #3F51B5;
            }
        """)
        main_layout.addWidget(self.role_combo)

        # Token file
        self.token_button = QPushButton("Select token file")
        self.token_button.setCursor(Qt.PointingHandCursor)
        self.token_button.clicked.connect(self.pick_file)
        self.token_button.setStyleSheet(self.button_style("#3F51B5"))
        main_layout.addWidget(self.token_button)

        self.token_label = QLabel("No file selected")
        self.token_label.setStyleSheet("color: #9E9E9E; font-size: 12px;")
        main_layout.addWidget(self.token_label)

        # Password with eye toggle
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
            }
        """)
        pw_layout.addWidget(self.eye_button)
        main_layout.addLayout(pw_layout)

        # Submit button
        self.submit_button = QPushButton("Register")
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setStyleSheet(self.gradient_button_style())
        main_layout.addWidget(self.submit_button)

        # Back to login
        self.login_button = QPushButton("Back to Login")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.navigate_to_login.emit)
        self.login_button.setStyleSheet("""
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
        main_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        main_layout.addStretch()
        self.setLayout(main_layout)

        # Gradient background
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
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def pick_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select token path",
            "hearmypaper_token.bin",
            "Binary Files (*.bin);;All Files (*)"
        )
        if file_path:
            self.token_path = file_path
            self.token_label.setText(file_path)

    def on_submit(self):
        if not self.username_input.text():
            QMessageBox.warning(self, "Error", "Please enter a username")
            return
        if not self.token_path:
            QMessageBox.warning(self, "Error", "Please select a token file path")
            return
        if not self.password_input.text():
            QMessageBox.warning(self, "Error", "Please enter a password")
            return

        error = self.auth_service.register(
            self.username_input.text(),
            self.role_combo.currentText(),
            self.token_path,
            self.password_input.text()
        )

        if not error:
            QMessageBox.information(self, "Success", "Registration successful")
            self.navigate_to_login.emit()
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
