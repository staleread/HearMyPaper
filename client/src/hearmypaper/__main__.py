# import sys
# import os
# from PyQt5.QtWidgets import QApplication
# from  ui.main_window import MainWindow
#
# sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
#
# from services.auth_service import register, login
#
#
# class AuthService:
#     def register(self, username, role, token_path, password):
#         return register(username, role, token_path, password)
#
#     def login(self, token_path, password):
#         return login(token_path, password)
#
#
# class MainApp:
#     def __init__(self):
#         self.auth_service = AuthService()
#         self.main_window = MainWindow(self.auth_service)
#
#     def show_login(self):
#         self.main_window.show_login()
#         self.main_window.show()
#
#
# def main():
#     app = QApplication(sys.argv)
#     main_app = MainApp()
#     main_app.show_login()
#     sys.exit(app.exec_())
#
#
# if __name__ == "__main__":
#     main()
