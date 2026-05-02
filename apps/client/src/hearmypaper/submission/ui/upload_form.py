import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .. import service


def submission_upload_form_screen(navigator, project_id: int):
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

    title_input = toga.TextInput(
        placeholder="Title",
        style=Pack(flex=1),
    )

    file_input = toga.TextInput(
        placeholder="Path to file",
        readonly=True,
        style=Pack(flex=1),
    )

    async def show_error(message: str):
        dialog = toga.ErrorDialog(title="Error", message=message)
        await navigator.main_window.dialog(dialog)

    async def show_info(message: str):
        dialog = toga.InfoDialog(title="Success", message=message)
        await navigator.main_window.dialog(dialog)

    async def on_select_file(widget):
        try:
            file_path = await navigator.main_window.dialog(
                toga.OpenFileDialog(title="Select Submission File")
            )
            if file_path:
                file_input.value = str(file_path)
        except Exception as e:
            await show_error(f"File selection error: {e}")

    async def on_submit(widget):
        if not title_input.value.strip():
            await show_error("Title is required!")
            return

        if not file_input.value:
            await show_error("Please choose a file to submit!")
            return

        result = service.upload_submission(
            navigator.session, project_id, title_input.value, file_input.value
        )

        if result.is_ok():
            await show_info("Submission uploaded successfully!")
            navigator.navigate("submissions_catalog")
        else:
            await show_error(result.unwrap_err())

    def on_cancel(widget):
        navigator.navigate("submissions_catalog")

    children.extend(
        [
            toga.Label("Title:"),
            title_input,
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
