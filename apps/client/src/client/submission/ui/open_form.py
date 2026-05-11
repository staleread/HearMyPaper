import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def submission_open_form_screen(navigator, submission_id):
    """
    Screen to open submission with credentials.
    """
    children = [
        toga.Label(
            "Open Submission",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        ),
        toga.Label(
            f"Open submission #{submission_id} with system default application.",
            style=Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
        ),
    ]

    token_password_input = toga.PasswordInput(
        placeholder="Token password", style=Pack(flex=1)
    )

    async def show_error(message: str):
        dialog = toga.ErrorDialog(title="Error", message=message)
        await navigator.main_window.dialog(dialog)

    async def show_info(message: str):
        dialog = toga.InfoDialog(title="Success", message=message)
        await navigator.main_window.dialog(dialog)

    async def on_open(widget):
        await navigator.main_window.dialog(
            toga.InfoDialog(
                "Open Submission",
                "Submission viewing is not yet supported in this version.",
            )
        )
        navigator.navigate("submission_info", attempt_id=submission_id)

    def on_cancel(widget):
        navigator.navigate("submission_info", attempt_id=submission_id)

    children.extend(
        [
            toga.Label("Token Password:"),
            token_password_input,
            toga.Box(
                children=[
                    toga.Button(
                        "Open",
                        on_press=lambda w: asyncio.create_task(on_open(w)),
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
