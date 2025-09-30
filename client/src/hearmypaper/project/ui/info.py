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

    actions = [("Edit", on_edit_project)]

    return item_info_screen(
        title="Project Details",
        data=data,
        on_back=lambda w: navigator.navigate("projects_catalog"),
        actions=actions,
    )
