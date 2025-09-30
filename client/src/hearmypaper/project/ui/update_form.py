import toga
from datetime import datetime

from ..service import update_project
from ..dto import ProjectUpdateDto
from ...shared.ui.components.datetime_picker import DateTimePicker


def project_edit_form_screen(navigator, project_data):
    children = [
        toga.Label(
            f"Edit Project: {project_data.get('title', '')}",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", margin=(0, 0, 10, 0)
            ),
        )
    ]

    title_input = toga.TextInput(value=project_data.get("title", ""))
    syllabus_input = toga.MultilineTextInput(
        value=project_data.get("syllabus_summary", ""),
        style=toga.style.Pack(height=100),
    )
    description_input = toga.MultilineTextInput(
        value=project_data.get("description", ""), style=toga.style.Pack(height=100)
    )

    instructor_email_input = toga.TextInput(
        value=project_data.get("instructor_email", ""),
        placeholder="Instructor Email (e.g., john.doe@university.edu)",
    )

    current_deadline = project_data.get("deadline", "")
    initial_deadline = None
    if current_deadline:
        try:
            initial_deadline = datetime.fromisoformat(
                current_deadline.replace("Z", "+00:00")
            )
        except ValueError:
            initial_deadline = None

    deadline_picker = DateTimePicker(initial_value=initial_deadline)

    async def on_submit(widget):
        if not all(
            [
                title_input.value,
                syllabus_input.value,
                description_input.value,
                instructor_email_input.value,
            ]
        ):
            dialog = toga.ErrorDialog(
                title="Error", message="Please fill in all required fields"
            )
            await navigator.main_window.dialog(dialog)
            return

        instructor_email = instructor_email_input.value.strip()
        if "@" not in instructor_email or "." not in instructor_email:
            dialog = toga.ErrorDialog(
                title="Error", message="Please enter a valid email address"
            )
            await navigator.main_window.dialog(dialog)
            return

        try:
            deadline = deadline_picker.value.isoformat()

            project_dto = ProjectUpdateDto(
                title=title_input.value,
                syllabus_summary=syllabus_input.value,
                description=description_input.value,
                instructor_email=instructor_email,
                deadline=deadline,
            )

            result = update_project(navigator.session, project_data["id"], project_dto)

            if result.is_ok():
                success_dialog = toga.InfoDialog(
                    title="Success", message="Project updated successfully"
                )
                await navigator.main_window.dialog(success_dialog)
                navigator.navigate("project_info", project_data["id"])
            else:
                error_dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to update project: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(error_dialog)
        except Exception as e:
            exception_dialog = toga.ErrorDialog(
                title="Error", message=f"Invalid input: {e}"
            )
            await navigator.main_window.dialog(exception_dialog)

    def on_cancel(widget):
        navigator.navigate("project_info", project_data["id"])

    children.extend(
        [
            toga.Label("Title:"),
            title_input,
            toga.Label("Syllabus Summary:"),
            syllabus_input,
            toga.Label("Description:"),
            description_input,
            toga.Label("Instructor Email:"),
            toga.Label(
                "(Enter the email address of the instructor)",
                style=toga.style.Pack(font_size=10, color="#666666"),
            ),
            instructor_email_input,
            toga.Label("Deadline:"),
            deadline_picker.widget,
            toga.Box(
                children=[
                    toga.Button("Update Project", on_press=on_submit),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=toga.style.Pack(
                    direction=toga.style.pack.ROW, margin=(10, 0, 0, 0)
                ),
            ),
        ]
    )

    return toga.ScrollContainer(
        content=toga.Box(
            children=children,
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
        )
    )
