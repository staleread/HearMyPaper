import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from uuid import UUID


def conversion_download_form_screen(navigator, conversion_id):
    if isinstance(conversion_id, str):
        conversion_id = UUID(conversion_id)

    password_input = toga.PasswordInput(style=Pack(flex=1))

    async def on_download(widget):
        password = password_input.value
        if not password:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", "Please enter your password")
            )
            return

        try:
            local_path = await navigator.download_conversion_use_case(
                conversion_id, password
            )
            await navigator.main_window.dialog(
                toga.InfoDialog(
                    "Success", f"Audio file downloaded and unsealed to: {local_path}"
                )
            )
            navigator.navigate("conversions_catalog")
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to download conversion: {e}")
            )

    return toga.Box(
        children=[
            toga.Label(
                "Download Conversion",
                style=Pack(font_size=14, font_weight="bold", margin_bottom=20),
            ),
            toga.Label("Enter your password to unseal the audio file:"),
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
                        on_press=lambda w: asyncio.create_task(on_download(w)),
                        style=Pack(flex=1),
                    ),
                    toga.Button(
                        "Cancel",
                        on_press=lambda w: navigator.navigate("conversions_catalog"),
                        style=Pack(flex=1),
                    ),
                ],
                style=Pack(direction=ROW, gap=10),
            ),
        ],
        style=Pack(direction=COLUMN, margin=20),
    )
