import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from ..service import login


def login_screen(navigator):
    title_label = toga.Label(
        "Login", style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0))
    )

    subtitle_label = toga.Label(
        "Login to access your submissions and projects",
        style=Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
    )

    token_path_input = toga.TextInput(
        placeholder="Path to credentials token file",
        readonly=True,
        style=Pack(flex=1),
    )

    password = toga.PasswordInput(
        placeholder="Password",
        style=Pack(flex=1),
    )

    async def on_select_token(widget):
        try:
            file_path = await navigator.main_window.dialog(
                toga.OpenFileDialog(
                    title="Select Credentials Token File", file_types=["bin"]
                )
            )
            if file_path:
                token_path_input.value = str(file_path)
        except Exception as e:
            dialog = toga.ErrorDialog(
                title="Error", message=f"File selection error: {e}"
            )
            await navigator.main_window.dialog(dialog)

    async def on_submit(widget):
        if not token_path_input.value:
            dialog = toga.ErrorDialog(title="Error", message="Please select token file")
            await navigator.main_window.dialog(dialog)
            return

        if not password.value:
            dialog = toga.ErrorDialog(title="Error", message="Please enter password")
            await navigator.main_window.dialog(dialog)
            return

        result = login(navigator.session, token_path_input.value, password.value)

        if result.is_ok():
            # Store credentials path in navigator
            navigator.credentials_path = token_path_input.value
            navigator.navigate("resource_catalog")
            return

        dialog = toga.ErrorDialog(title="Login Failed", message=result.unwrap_err())
        await navigator.main_window.dialog(dialog)

    return toga.Box(
        children=[
            title_label,
            subtitle_label,
            toga.Label("Credentials Token:"),
            toga.Box(
                children=[
                    token_path_input,
                    toga.Button("Browse", on_press=on_select_token),
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            toga.Label("Password:"),
            password,
            toga.Button("Login", on_press=on_submit),
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )
