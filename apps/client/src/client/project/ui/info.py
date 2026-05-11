import asyncio
import toga
from result import Ok
from ...shared.ui.item_info_screen import item_info_screen
from uuid import UUID


def project_info_screen(navigator, project_id):
    if isinstance(project_id, str):
        project_id = UUID(project_id)

    container = toga.Box(children=[toga.Label("Loading project details...")])

    async def load_project():
        try:
            project = await navigator.get_project_use_case(project_id)

            project_data = {
                "id": str(project.id),
                "title": project.title,
                "description": project.description,
                "instructor_id": project.instructor_id,
                "deadline": project.deadline.isoformat(),
            }

            def on_edit_project(w):
                navigator.navigate("project_edit_form", project_data)

            def on_manage_students(w):
                navigator.navigate("manage_students_form", project_id)

            def on_upload_submission(w):
                navigator.navigate("submission_upload_form", project_id=project_id)

            def on_view_attempts(w):
                navigator.navigate("submissions_catalog", project_id=project_id)

            actions = [
                ("Edit", on_edit_project),
                ("Manage Students", on_manage_students),
                ("Upload Submission", on_upload_submission),
                ("View Attempts", on_view_attempts),
            ]

            info_screen = item_info_screen(
                title="Project Details",
                data=Ok(project_data),
                on_back=lambda w: navigator.navigate("projects_catalog"),
                actions=actions,
            )
            navigator.main_window.content = info_screen
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to load project: {e}")
            )
            navigator.navigate("projects_catalog")

    asyncio.create_task(load_project())
    return container
