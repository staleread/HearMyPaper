import toga
from datetime import datetime, timedelta
from ..api import create_project


def project_create_form_screen(navigator):
    """Project creation form screen with manual inputs (similar to user_create_form_screen)"""

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
    instructor_input = toga.TextInput(placeholder="Instructor ID (number)")
    deadline_input = toga.TextInput(
        placeholder="Deadline (ISO format, e.g. 2025-12-15T23:59:59Z)"
    )

    async def on_submit(widget):
        # Validate inputs
        if not all(
            [
                title_input.value,
                syllabus_input.value,
                description_input.value,
                instructor_input.value,
            ]
        ):
            dialog = toga.ErrorDialog(
                title="Error", message="Please fill in all required fields"
            )
            await navigator.main_window.dialog(dialog)
            return

        try:
            instructor_id = int(instructor_input.value)
        except ValueError:
            dialog = toga.ErrorDialog(
                title="Error", message="Instructor ID must be a number"
            )
            await navigator.main_window.dialog(dialog)
            return

        # Use provided deadline or fallback to 30 days from now
        deadline = deadline_input.value
        if not deadline:
            deadline = (
                datetime.now().replace(microsecond=0) + timedelta(days=30)
            ).isoformat() + "Z"

        project_data = {
            "title": title_input.value,
            "syllabus_summary": syllabus_input.value,
            "description": description_input.value,
            "instructor_id": instructor_id,
            "deadline": deadline,
        }

        try:
            result = create_project(navigator.session, project_data)

            if result.is_ok():
                response = result.unwrap()
                dialog = toga.InfoDialog(
                    title="Success",
                    message=f"Project created successfully!\nProject ID: {response.id}",
                )
                await navigator.main_window.dialog(dialog)
                navigator.navigate("projects_catalog")
            else:
                dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to create project: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(dialog)
        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Invalid input: {e}")
            await navigator.main_window.dialog(dialog)

    def on_cancel(widget):
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
            toga.Label("Instructor ID:"),
            instructor_input,
            toga.Label("Deadline (optional, ISO):"),
            deadline_input,
            toga.Box(
                children=[
                    toga.Button("Create Project", on_press=on_submit),
                    toga.Button("Cancel", on_press=on_cancel),
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
