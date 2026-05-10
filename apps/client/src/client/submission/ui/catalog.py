import asyncio
import toga
from ...shared.ui.catalog_screen import catalog_screen
from result import Ok
from uuid import UUID


def submissions_catalog_screen(navigator, project_id):
    if isinstance(project_id, str):
        project_id = UUID(project_id)

    def on_row_activate(row):
        navigator.navigate("submission_info", getattr(row, "id"))

    # Initial empty state
    data = Ok([])

    catalog = catalog_screen(
        title="Lab Attempts",
        headings=["Attempt ID", "Student ID", "Submitted At", "On Time", "Grade"],
        data=data,
        on_back=lambda w: navigator.navigate("project_info", project_id),
        actions=[],
        on_activate=on_row_activate,
    )

    async def load_data():
        try:
            attempts = await navigator.get_project_attempts_use_case(project_id)
            table = catalog.children[1]
            table.data = [
                {
                    "id": a.id,
                    "attempt_id": str(a.id),
                    "student_id": a.student_id,
                    "submitted_at": a.submitted_at.isoformat(),
                    "on_time": "Yes" if a.is_on_time else "No",
                    "grade": str(a.grade) if a.grade is not None else "N/A",
                }
                for a in attempts
            ]
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to load attempts: {e}")
            )

    asyncio.create_task(load_data())

    return catalog
