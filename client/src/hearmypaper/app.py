import toga

from .audit.ui.audit_screen import audit_catalog_screen
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
from .submissions.ui.download_form import submission_download_form
from .submissions.ui.catalog import submissions_catalog_screen
from .submissions.ui.upload_file import submission_upload_form


class HearMyPaper(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="HearMyPaper")
        self.navigator = Navigator(self.main_window, self.paths)

        self.navigator.register_screen("login", login_screen)
        self.navigator.register_screen("resource_catalog", resource_catalog_screen)
        self.navigator.register_screen("users_catalog", users_catalog_screen)
        self.navigator.register_screen("user_create_form", user_create_form_screen)
        self.navigator.register_screen("projects_catalog", projects_catalog_screen)
        self.navigator.register_screen("audit_catalog", audit_catalog_screen)
        self.navigator.register_screen(
            "submissions_catalog", submissions_catalog_screen
        )  #
        self.navigator.register_screen("submission_upload_form", submission_upload_form)

        self.navigator.register_screen(
            "project_create_form", project_create_form_screen
        )
        self.navigator.register_screen(
            "submission_download_form", submission_download_form
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
