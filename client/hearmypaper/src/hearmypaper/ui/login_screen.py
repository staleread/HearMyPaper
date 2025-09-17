import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from hearmypaper.services.auth_service import login


def login_screen(navigator):
    password = toga.PasswordInput(placeholder="Password")

    token_label = toga.Label("No file selected")

    async def pick_file(widget):
        dialog = toga.OpenFileDialog(title="Select token path", multiple_select=False)
        file_path = await navigator.main_window.dialog(dialog)
        if file_path:
            token_label.text = file_path

    async def on_submit(widget):
        error = login(token_label.text, password.value)

        if not error:
            dialog = toga.InfoDialog(title="Info", message="Login successful")

            return await navigator.main_window.dialog(dialog)

        dialog = toga.ErrorDialog(title="Oops", message=error)
        await navigator.main_window.dialog(dialog)

    return toga.Box(
        children=[
            toga.Label("Login", style=Pack(padding=(0, 0, 10, 0))),
            toga.Button("Select token path", on_press=pick_file),
            token_label,
            password,
            toga.Button("Submit", on_press=on_submit),
            toga.Button("Register", on_press=lambda w: navigator.navigate("register")),
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )
