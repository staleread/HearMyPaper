import toga
from datetime import datetime, timedelta

from ..service import create_project
from ..dto import ProjectCreateDto
from ...shared.ui.components.datetime_picker import DateTimePicker


def project_create_form_screen(navigator):
    children = [
        toga.Label(
            "Create New Project",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", margin=(0, 0, 10, 0)
            ),
        )
    ]

    title_input = toga.TextInput(placeholder="Project Title")
    syllabus_input = toga.MultilineTextInput(placeholder="Brief syllabus summary")
    description_input = toga.MultilineTextInput(
        placeholder="Detailed project description"
    )

    instructor_email_input = toga.TextInput(
        placeholder="Instructor Email (e.g., john.doe@university.edu)"
    )

    default_deadline = datetime.now() + timedelta(days=30)
    deadline_picker = DateTimePicker(initial_value=default_deadline)

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

        deadline = deadline_picker.value.isoformat() + "Z"

        project_dto = ProjectCreateDto(
            title=title_input.value,
            syllabus_summary=syllabus_input.value,
            description=description_input.value,
            instructor_email=instructor_email,
            deadline=deadline,
        )

        try:
            result = create_project(navigator.session, project_dto)

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

    def on_cancel(widget):
        navigator.navigate("projects_catalog")

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
                    toga.Button("Create Project", on_press=on_submit),
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
