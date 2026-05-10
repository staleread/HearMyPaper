from ...shared.ui.catalog_screen import catalog_screen
from result import Ok


def projects_catalog_screen(navigator):
    def on_row_activate(row):
        navigator.navigate("project_info", getattr(row, "id"))

    async def load_data():
        try:
            projects = await navigator.get_my_projects_use_case()
            return [{"id": p.id, "title": p.title} for p in projects]
        except Exception as e:
            await navigator.main_window.dialog(
                navigator.toga.ErrorDialog("Error", f"Failed to load projects: {e}")
            )
            return []

    actions = [("Create Project", lambda w: navigator.navigate("project_create_form"))]

    return catalog_screen(
        title="Projects",
        headings=["Title"],
        data=Ok([]),
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=actions,
        on_activate=on_row_activate,
        on_refresh=load_data,
        empty_message="No projects found. Use 'Create Project' to add one.",
    )
