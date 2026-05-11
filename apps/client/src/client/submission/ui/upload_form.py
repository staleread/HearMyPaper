import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from uuid import UUID


def submission_upload_form_screen(navigator, project_id):
    if isinstance(project_id, str):
        project_id = UUID(project_id)

    children = [
        toga.Label(
            "Upload Submission",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        ),
        toga.Label(
            "Securely upload your project file for instructor review.",
            style=Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
        ),
    ]

    file_input = toga.TextInput(
        placeholder="Path to file",
        readonly=True,
        style=Pack(flex=1),
    )

    async def on_select_file(widget):
        try:
            file_path = await navigator.main_window.dialog(
                toga.OpenFileDialog(title="Select Submission File")
            )
            if file_path:
                file_input.value = str(file_path)
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"File selection error: {e}")
            )

    async def on_submit(widget):
        if not file_input.value:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", "Please choose a file to submit!")
            )
            return

        widget.enabled = False
        try:
            await navigator.upload_submission_use_case(
                project_id=project_id, file_path=file_input.value
            )
            await navigator.main_window.dialog(
                toga.InfoDialog("Success", "Submission uploaded successfully!")
            )
            navigator.navigate("project_info", project_id)
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Upload failed: {e}")
            )
        finally:
            widget.enabled = True

    def on_cancel(widget):
        navigator.navigate("project_info", project_id)

    children.extend(
        [
            toga.Label("Submission File:"),
            toga.Box(
                children=[
                    file_input,
                    toga.Button("Browse", on_press=on_select_file),
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            toga.Box(
                children=[
                    toga.Button(
                        "Submit", on_press=lambda w: asyncio.create_task(on_submit(w))
                    ),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=Pack(direction=ROW, margin=(20, 0, 0, 0), gap=10),
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
