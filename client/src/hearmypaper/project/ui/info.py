from result import is_ok
from hearmypaper.shared.ui.item_info_screen import item_info_screen
from ..service import get_project


def project_info_screen(navigator, project_id):
    data = get_project(navigator.session, project_id).map(
        lambda project: project.model_dump()
    )

    def on_edit_project():
        if is_ok(data):
            navigator.navigate("project_edit_form", data.unwrap())

    def on_manage_students():
        navigator.navigate("manage_students_form", project_id)

    def on_upload_submission():
        navigator.navigate("submission_upload_form", project_id=project_id)

    actions = [
        ("Edit", on_edit_project),
        ("Manage Students", on_manage_students),
        ("Upload Submission", on_upload_submission),
    ]

    return item_info_screen(
        title="Project Details",
        data=data,
        on_back=lambda w: navigator.navigate("projects_catalog"),
        actions=actions,
    )
