import toga
from ..api import update_project
from ...shared.ui.form_screen import form_screen


def project_edit_form_screen(navigator, project_data: dict):
    """Project edit form screen"""
    fields = [
        {
            "name": "title",
            "label": "Title",
            "type": "text",
            "value": project_data.get("title", ""),
        },
        {
            "name": "syllabus_summary",
            "label": "Syllabus Summary",
            "type": "multiline",
            "value": project_data.get("syllabus_summary", ""),
        },
        {
            "name": "description",
            "label": "Description",
            "type": "multiline",
            "value": project_data.get("description", ""),
        },
        {
            "name": "instructor_id",
            "label": "Instructor ID",
            "type": "number",
            "value": str(project_data.get("instructor_id", "")),
        },
        {
            "name": "deadline",
            "label": "Deadline (ISO format)",
            "type": "text",
            "value": project_data.get("deadline", ""),
        },
    ]

    async def on_submit(form_data, nav):
        try:
            # Process form data
            update_data = {
                "title": form_data["title"],
                "syllabus_summary": form_data["syllabus_summary"],
                "description": form_data["description"],
                "instructor_id": int(form_data["instructor_id"]),
                "deadline": form_data["deadline"],
            }

            result = update_project(navigator.session, project_data["id"], update_data)

            if result.is_ok():
                dialog = toga.InfoDialog(
                    title="Success", message="Project updated successfully"
                )
                await nav.main_window.dialog(dialog)
                nav.navigate_with_data("project_info", project_data["id"])
            else:
                dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to update project: {result.unwrap_err()}",
                )
                await nav.main_window.dialog(dialog)
        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Invalid input: {e}")
            await nav.main_window.dialog(dialog)

    def on_cancel(nav):
        nav.navigate_with_data("project_info", project_data["id"])

    return form_screen(
        title=f"Edit Project: {project_data.get('title', '')}",
        fields=fields,
        navigator=navigator,
        on_submit=lambda form_data, nav: navigator.main_window.app.add_background_task(
            lambda: on_submit(form_data, nav)
        ),
        on_cancel=on_cancel,
    )
