import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def submission_unseal_form_screen(navigator, attempt_id):
    password_input = toga.PasswordInput(style=Pack(flex=1))

    async def on_unseal(widget):
        password = password_input.value
        if not password:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", "Please enter your password")
            )
            return

        try:
            local_path = await navigator.download_attempt_use_case(attempt_id, password)
            await navigator.main_window.dialog(
                toga.InfoDialog(
                    "Success", f"File downloaded and unsealed to: {local_path}"
                )
            )
            navigator.navigate("submission_info", attempt_id)
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to unseal submission: {e}")
            )

    return toga.Box(
        children=[
            toga.Label(
                "Unseal Submission",
                style=Pack(font_size=14, font_weight="bold", margin_bottom=20),
            ),
            toga.Label("Enter your password to unseal the file:"),
            toga.Box(
                children=[
                    toga.Label("Password:", style=Pack(width=100)),
                    password_input,
                ],
                style=Pack(direction=ROW, margin_bottom=10),
            ),
            toga.Box(
                children=[
                    toga.Button(
                        "Download & Unseal",
                        on_press=lambda w: asyncio.create_task(on_unseal(w)),
                        style=Pack(flex=1),
                    ),
                    toga.Button(
                        "Cancel",
                        on_press=lambda w: navigator.navigate(
                            "submission_info", attempt_id
                        ),
                        style=Pack(flex=1),
                    ),
                ],
                style=Pack(direction=ROW, gap=10),
            ),
        ],
        style=Pack(direction=COLUMN, margin=20),
    )
