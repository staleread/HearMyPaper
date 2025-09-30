from hearmypaper.shared.ui.catalog_screen import catalog_screen
from ..service import get_projects_list


def projects_catalog_screen(navigator):
    def on_row_activate(row):
        navigator.navigate("project_info", row.id)

    data = (
        get_projects_list(navigator.session)
        .map(lambda projects: [project.model_dump() for project in projects])
        .map_err(lambda err: f"Error loading projects: {err}")
    )

    actions = [("Create Project", lambda w: navigator.navigate("project_create_form"))]

    return catalog_screen(
        title="Projects",
        headings=["Title"],
        data=data,
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=actions,
        on_activate=on_row_activate,
    )
