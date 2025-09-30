import toga
from typing import Any, cast
from ..service import update_project_with_dto
from ..dto import ProjectUpdateDto


def project_edit_form_screen(navigator, project_data: dict):
    """Project edit form screen with instructor email input"""

    children = [
        toga.Label(
            f"Edit Project: {project_data.get('title', '')}",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", padding=(0, 0, 10, 0)
            ),
        )
    ]

    # Form inputs
    title_input = toga.TextInput(value=project_data.get("title", ""))
    syllabus_input = toga.MultilineTextInput(
        value=project_data.get("syllabus_summary", ""),
        style=toga.style.Pack(height=100),
    )
    description_input = toga.MultilineTextInput(
        value=project_data.get("description", ""), style=toga.style.Pack(height=100)
    )

    # Use email input - pre-populated with current instructor email
    instructor_email_input = toga.TextInput(
        value=project_data.get("instructor_email", ""),
        placeholder="Instructor Email (e.g., john.doe@university.edu)",
    )

    deadline_input = toga.TextInput(value=project_data.get("deadline", ""))

    async def on_submit(widget: toga.Widget) -> None:
        # Validate inputs
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

        # Basic email validation
        instructor_email = instructor_email_input.value.strip()
        if "@" not in instructor_email or "." not in instructor_email:
            dialog = toga.ErrorDialog(
                title="Error", message="Please enter a valid email address"
            )
            await navigator.main_window.dialog(dialog)
            return

        try:
            # Create DTO from form data
            project_dto = ProjectUpdateDto(
                title=title_input.value,
                syllabus_summary=syllabus_input.value,
                description=description_input.value,
                instructor_email=instructor_email,
                deadline=deadline_input.value,
            )

            result = update_project_with_dto(
                navigator.session, project_data["id"], project_dto
            )

            if result.is_ok():
                success_dialog = toga.InfoDialog(
                    title="Success", message="Project updated successfully"
                )
                await navigator.main_window.dialog(success_dialog)
                navigator.navigate_with_data("project_info", project_data["id"])
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

    def on_cancel(widget: toga.Widget) -> None:
        navigator.navigate_with_data("project_info", project_data["id"])

    # Build form manually
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
            toga.Label("Deadline (ISO format):"),
            deadline_input,
            toga.Box(
                children=[
                    toga.Button("Update Project", on_press=cast(Any, on_submit)),
                    toga.Button("Cancel", on_press=cast(Any, on_cancel)),
                ],
                style=toga.style.Pack(
                    direction=toga.style.pack.ROW, padding=(10, 0, 0, 0)
                ),
            ),
        ]
    )

    return toga.Box(
        children=children,
        style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
    )
