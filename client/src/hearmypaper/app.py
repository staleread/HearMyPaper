import toga

from .shared.utils.navigator import Navigator
from .auth.ui.login_screen import login_screen
from .shared.ui.resource_catalog import resource_catalog_screen
from .user.ui.catalog import users_catalog_screen
from .user.ui.info import user_info_screen
from .user.ui.create_form import user_create_form_screen
from .user.ui.update_form import user_edit_form_screen
from .project.ui.catalog import projects_catalog_screen
from .project.ui.info import project_info_screen
from .project.ui.create_form import project_create_form_screen
from .project.ui.update_form import project_edit_form_screen
from .project.ui.manage_students_form import manage_students_form_screen
from .pdf_to_audio.ui.form import pdf_to_audio_form_screen


class HearMyPaper(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="HearMyPaper")
        self.navigator = Navigator(self.main_window, self.paths)

        self.navigator.register_screen("login", login_screen)
        self.navigator.register_screen("resource_catalog", resource_catalog_screen)
        self.navigator.register_screen("users_catalog", users_catalog_screen)
        self.navigator.register_screen("user_create_form", user_create_form_screen)
        self.navigator.register_screen("projects_catalog", projects_catalog_screen)
        self.navigator.register_screen(
            "project_create_form", project_create_form_screen
        )

        self.navigator.register_screen("user_info", user_info_screen)
        self.navigator.register_screen("user_edit_form", user_edit_form_screen)
        self.navigator.register_screen("project_info", project_info_screen)
        self.navigator.register_screen("project_edit_form", project_edit_form_screen)
        self.navigator.register_screen(
            "manage_students_form", manage_students_form_screen
        )
        self.navigator.register_screen("pdf_to_audio_form", pdf_to_audio_form_screen)

        self.navigator.navigate("login")
        self.main_window.show()


def main():
    return HearMyPaper()
