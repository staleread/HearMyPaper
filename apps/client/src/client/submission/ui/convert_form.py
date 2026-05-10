import toga
import asyncio
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def submission_convert_form_screen(navigator, submission_id: int):
    """
    Convert submission PDF to audio.
    """
    children = [
        toga.Label(
            "PDF to Audio Converter",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        ),
        toga.Label(
            f"Convert submission #{submission_id} to audio",
            style=Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
        ),
    ]

    token_password_input = toga.PasswordInput(
        placeholder="Token password", style=Pack(flex=1)
    )

    output_file_input = toga.TextInput(
        placeholder="Output audio file path",
        readonly=True,
        style=Pack(flex=1),
    )

    # Speed slider with label
    speed_value_label = toga.Label("140 wpm", style=Pack(width=70))
    speed_slider = toga.Slider(
        min=80,
        max=300,
        value=140,
        style=Pack(flex=1),
    )

    # Status label for showing progress
    status_label = toga.Label(
        "",
        style=Pack(font_size=10, color="#0066cc", margin=(10, 0)),
    )

    def on_speed_change(widget):
        speed_value_label.text = f"{int(widget.value)} wpm"

    speed_slider.on_change = on_speed_change

    async def show_error(message: str):
        dialog = toga.ErrorDialog(title="Error", message=message)
        await navigator.main_window.dialog(dialog)

    async def show_info(message: str):
        dialog = toga.InfoDialog(title="Success", message=message)
        await navigator.main_window.dialog(dialog)

    async def on_select_output(widget):
        try:
            file_path = await navigator.main_window.save_file_dialog(
                title="Save Audio File As",
                suggested_filename=f"submission_{submission_id}.wav",
                file_types=["wav"],
            )
            if file_path:
                output_file_input.value = str(file_path)
        except Exception as e:
            await show_error(f"File selection error: {e}")

    async def on_convert(widget):
        await navigator.main_window.dialog(
            toga.InfoDialog(
                "Audio Conversion",
                "Submission to audio conversion is not yet supported in this version. "
                "Please check for updates later.",
            )
        )
        navigator.navigate("submission_info", submission_id=submission_id)

    def on_cancel(widget):
        navigator.navigate("submission_info", submission_id=submission_id)

    children.extend(
        [
            toga.Label("Token Password:"),
            token_password_input,
            toga.Label("Speech Rate:"),
            toga.Box(
                children=[
                    speed_slider,
                    speed_value_label,
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            toga.Label("Output Audio File:"),
            toga.Box(
                children=[
                    output_file_input,
                    toga.Button("Browse", on_press=on_select_output),
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            status_label,
            toga.Box(
                children=[
                    toga.Button(
                        "Convert", on_press=lambda w: asyncio.create_task(on_convert(w))
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
