import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from ..service import download_submission
from ...auth.utils import get_user_credentials


def submission_download_form_screen(navigator, submission_id):
    children = [
        toga.Label(
            "Download Submission",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        ),
        toga.Label(
            "Download the submitted project file.",
            style=Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
        ),
    ]

    token_path_input = toga.TextInput(
        placeholder="Path to credentials token file",
        readonly=True,
        style=Pack(flex=1),
    )

    token_password_input = toga.PasswordInput(
        placeholder="Token password", style=Pack(flex=1)
    )

    async def show_error(message: str):
        dialog = toga.ErrorDialog(title="Error", message=message)
        await navigator.main_window.dialog(dialog)

    async def show_info(message: str):
        dialog = toga.InfoDialog(title="Success", message=message)
        await navigator.main_window.dialog(dialog)

    async def on_select_token(widget):
        try:
            file_path = await navigator.main_window.open_file_dialog(
                title="Select Credentials Token File"
            )
            if file_path:
                token_path_input.value = str(file_path)
        except Exception as e:
            await show_error(f"File selection error: {e}")

    async def on_download(widget):
        if not token_path_input.value:
            await show_error("Please select credentials token file")
            return

        if not token_password_input.value:
            await show_error("Please enter token password")
            return

        try:
            # Get private key from credentials
            _, private_key_bytes = get_user_credentials(
                token_path_input.value, token_password_input.value
            )

            result = download_submission(
                navigator.session, submission_id, private_key_bytes
            )

            if result.is_ok():
                await show_info(f"File saved to: {result.unwrap()}")
                navigator.navigate("submission_info", submission_id=submission_id)
            else:
                await show_error(result.unwrap_err())
        except Exception as e:
            await show_error(f"Download failed: {e}")

    def on_cancel(widget):
        navigator.navigate("submission_info", submission_id=submission_id)

    children.extend(
        [
            toga.Label("Credentials Token:"),
            toga.Box(
                children=[
                    token_path_input,
                    toga.Button("Browse", on_press=on_select_token),
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            toga.Label("Token Password:"),
            token_password_input,
            toga.Box(
                children=[
                    toga.Button(
                        "Download",
                        on_press=lambda w: asyncio.create_task(on_download(w)),
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
