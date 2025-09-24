from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QGraphicsOpacityEffect, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, Qt, QPropertyAnimation, QEasingCurve


class LoginScreen(QWidget):
    navigate_to_register = pyqtSignal()

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.token_path = ""
        self.init_ui()
        self.center_window()
        self.animate_widgets()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(420, 500)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(40, 40, 40, 40)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.title_label = QLabel("Welcome Back")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #3F51B5;
        """)
        main_layout.addWidget(self.title_label)

        self.token_button = QPushButton("Select Token File")
        self.token_button.clicked.connect(self.pick_file)
        self.token_button.setCursor(Qt.PointingHandCursor)
        self.token_button.setStyleSheet(self.button_style("#3F51B5"))
        main_layout.addWidget(self.token_button)

        self.token_label = QLabel("No file selected")
        self.token_label.setStyleSheet("color: #9E9E9E; font-size: 12px;")
        self.token_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.token_label)

        # Password input with simple eye button
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

        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.setStyleSheet(self.gradient_button_style())
        main_layout.addWidget(self.submit_button)

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
        main_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

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
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def animate_widgets(self):
        for widget in [self.title_label, self.token_button, self.token_label,
                       self.password_input, self.submit_button, self.register_button, self.eye_button]:
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(800)
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.start()
            widget.anim = anim

    def pick_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select token path", "", "All Files (*)"
        )
        if file_path:
            self.token_path = file_path
            self.token_label.setText(file_path)

    def on_submit(self):
        if not self.token_path:
            QMessageBox.warning(self, "Error", "Please select a token file")
            return
        if not self.password_input.text():
            QMessageBox.warning(self, "Error", "Please enter a password")
            return
        error = self.auth_service.login(self.token_path, self.password_input.text())
        if not error:
            QMessageBox.information(self, "Success", "Login successful")
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


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    class DummyAuth:
        def login(self, token, password):
            if password == "1234":
                return None
            return "Invalid credentials"

    app = QApplication(sys.argv)
    window = LoginScreen(DummyAuth())
    window.show()
    sys.exit(app.exec_())
