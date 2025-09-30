import toga
from ..api import get_projects
from ...shared.ui.catalog_screen import catalog_screen


def projects_catalog_screen(navigator):
    """Projects catalog screen"""
    result = get_projects(navigator.session)

    if result.is_err():
        return toga.Box(
            children=[
                toga.Label(f"Error loading projects: {result.unwrap_err()}"),
                toga.Button(
                    "← Back", on_press=lambda w: navigator.navigate("resource_catalog")
                ),
            ],
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
        )

    projects = result.unwrap()
    # Convert to dict list for compatibility with catalog_screen
    projects_dict = [project.model_dump() for project in projects]

    def on_project_click(project, nav):
        nav.navigate_with_data("project_info", project["id"])

    def on_create_project(nav):
        nav.navigate("project_create_form")

    actions = [("Create Project", on_create_project)]

    return catalog_screen(
        title="Projects",
        items=projects_dict,
        navigator=navigator,
        on_item_click=on_project_click,
        actions=actions,
        parent_catalog="Resources",
    )
