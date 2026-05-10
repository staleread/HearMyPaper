import asyncio
from ...shared.ui.catalog_screen import catalog_screen
from result import Ok


def projects_catalog_screen(navigator):
    def on_row_activate(row):
        navigator.navigate("project_info", getattr(row, "id"))

    # Initial empty state
    data = Ok([])

    actions = [("Create Project", lambda w: navigator.navigate("project_create_form"))]

    catalog = catalog_screen(
        title="Projects",
        headings=["Title"],
        data=data,
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=actions,
        on_activate=on_row_activate,
    )

    async def load_data():
        try:
            projects = await navigator.get_my_projects_use_case()
            # The catalog is a Box, children[1] is the Table
            table = catalog.children[1]
            table.data = [{"id": p.id, "title": p.title} for p in projects]
        except Exception as e:
            await navigator.main_window.dialog(
                navigator.toga.ErrorDialog("Error", f"Failed to load projects: {e}")
            )

    asyncio.create_task(load_data())

    return catalog
