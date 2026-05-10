import toga
from datetime import datetime
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from uuid import UUID

from ...shared.ui.components.datetime_picker import DateTimePicker


def project_edit_form_screen(navigator, project_data):
    children = [
        toga.Label(
            "Edit Project",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        )
    ]

    project_id = project_data["id"]
    if isinstance(project_id, str):
        project_id = UUID(project_id)

    title_input = toga.TextInput(value=project_data.get("title", ""))
    description_input = toga.MultilineTextInput(
        value=project_data.get("description", ""), style=Pack(height=150)
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
        if not all([title_input.value, description_input.value]):
            await navigator.main_window.dialog(
                toga.ErrorDialog(
                    title="Error", message="Please fill in all required fields"
                )
            )
            return

        try:
            deadline = deadline_picker.value

            await navigator.update_project_use_case(
                project_id=project_id,
                title=title_input.value,
                description=description_input.value,
                deadline=deadline,
            )

            await navigator.main_window.dialog(
                toga.InfoDialog(
                    title="Success", message="Project updated successfully!"
                )
            )
            navigator.navigate("project_info", project_id)
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog(
                    title="Error", message=f"Failed to update project: {e}"
                )
            )

    def on_cancel(widget):
        navigator.navigate("project_info", project_id)

    children.extend(
        [
            toga.Label("Title:"),
            title_input,
            toga.Label("Description:"),
            description_input,
            toga.Label("Deadline:"),
            deadline_picker.widget,
            toga.Box(
                children=[
                    toga.Button("Update Project", on_press=on_submit),
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
