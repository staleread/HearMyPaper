import toga
from datetime import datetime, timedelta
from typing import Any, cast

from ..service import create_project_with_dto
from ..dto import ProjectCreateDto


def project_create_form_screen(navigator):
    """Project creation form screen with instructor dropdown using user service"""

    children = [
        toga.Label(
            "Create New Project",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", padding=(0, 0, 10, 0)
            ),
        )
    ]

    # Form inputs
    title_input = toga.TextInput(placeholder="Project Title")
    syllabus_input = toga.MultilineTextInput(placeholder="Brief syllabus summary")
    description_input = toga.MultilineTextInput(
        placeholder="Detailed project description"
    )

    # Use email input instead of dropdown (Curator can't see user list)
    instructor_email_input = toga.TextInput(
        placeholder="Instructor Email (e.g., john.doe@university.edu)"
    )

    deadline_input = toga.TextInput(
        placeholder="Deadline (ISO format, e.g. 2025-12-15T23:59:59Z)"
    )

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

        # Use provided deadline or fallback to 30 days from now
        deadline = deadline_input.value
        if not deadline:
            deadline = (
                datetime.now().replace(microsecond=0) + timedelta(days=30)
            ).isoformat() + "Z"

        # Create DTO from form data
        project_dto = ProjectCreateDto(
            title=title_input.value,
            syllabus_summary=syllabus_input.value,
            description=description_input.value,
            instructor_email=instructor_email,
            deadline=deadline,
        )

        try:
            result = create_project_with_dto(navigator.session, project_dto)

            if result.is_ok():
                response = result.unwrap()
                success_dialog = toga.InfoDialog(
                    title="Success",
                    message=f"Project created successfully!\nProject ID: {response.id}",
                )
                await navigator.main_window.dialog(success_dialog)
                navigator.navigate("projects_catalog")
            else:
                error_dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to create project: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(error_dialog)
        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Invalid input: {e}")
            await navigator.main_window.dialog(dialog)

    def on_cancel(widget: toga.Widget) -> None:
        navigator.navigate("projects_catalog")

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
            toga.Label("Deadline (optional, ISO):"),
            deadline_input,
            toga.Box(
                children=[
                    toga.Button("Create Project", on_press=cast(Any, on_submit)),
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
