import toga
from typing import cast, Any
from ..api import get_project
from ...shared.ui.item_info_screen import item_info_screen


def project_info_screen(navigator, project_id: int):
    """Project info screen"""
    result = get_project(navigator.session, project_id)

    if result.is_err():

        def handle_back(widget: toga.Widget) -> None:
            navigator.navigate("projects_catalog")

        return toga.Box(
            children=[
                toga.Label(f"Error loading project: {result.unwrap_err()}"),
                toga.Button("← Back", on_press=cast(Any, handle_back)),
            ],
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
        )

    project_data = result.unwrap()
    # Convert to dict for compatibility with item_info_screen
    project_dict = project_data.model_dump()

    def on_edit_project(item_data, nav):
        nav.navigate_with_data("project_edit_form", item_data)

    def on_delete_project(item_data, nav):
        # This should never be called since delete is marked as unsupported
        pass

    actions = [
        ("Edit", on_edit_project, True),
        ("Delete", on_delete_project, False),  # Delete not supported
    ]

    return item_info_screen(
        title=f"Project: {project_data.title}",
        item_data=project_dict,
        navigator=navigator,
        actions=actions,
        back_target="projects_catalog",
    )
