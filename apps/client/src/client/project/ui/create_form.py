import toga
from datetime import datetime, timedelta
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from ...shared.ui.components.datetime_picker import DateTimePicker


def project_create_form_screen(navigator):
    children = [
        toga.Label(
            "Create New Project",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        )
    ]

    title_input = toga.TextInput(placeholder="Project Title")
    description_input = toga.MultilineTextInput(
        placeholder="Detailed project description", style=Pack(height=150)
    )
    instructor_id_input = toga.TextInput(placeholder="Instructor User ID")

    default_deadline = datetime.now() + timedelta(days=30)
    deadline_picker = DateTimePicker(initial_value=default_deadline)

    async def on_submit(widget):
        if not all(
            [title_input.value, description_input.value, instructor_id_input.value]
        ):
            await navigator.main_window.dialog(
                toga.ErrorDialog(
                    title="Error", message="Please fill in all required fields"
                )
            )
            return

        try:
            deadline = deadline_picker.value

            await navigator.create_project_use_case(
                title=title_input.value,
                description=description_input.value,
                instructor_id=instructor_id_input.value,
                deadline=deadline,
            )

            await navigator.main_window.dialog(
                toga.InfoDialog(
                    title="Success", message="Project created successfully!"
                )
            )
            navigator.navigate("projects_catalog")
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog(
                    title="Error", message=f"Failed to create project: {e}"
                )
            )

    def on_cancel(widget):
        navigator.navigate("projects_catalog")

    children.extend(
        [
            toga.Label("Title:"),
            title_input,
            toga.Label("Description:"),
            description_input,
            toga.Label("Instructor ID:"),
            instructor_id_input,
            toga.Label("Deadline:"),
            deadline_picker.widget,
            toga.Box(
                children=[
                    toga.Button("Create Project", on_press=on_submit),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=Pack(direction=ROW, margin=(10, 0, 0, 0), gap=10),
            ),
        ]
    )

    return toga.ScrollContainer(
        horizontal=False,
        content=toga.Box(
            children=children,
            style=Pack(direction=COLUMN, margin=20, gap=10),
        ),
    )
