import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from ..service import login


def login_screen(navigator):
    password = toga.PasswordInput(placeholder="Password")

    token_label = toga.Label("No file selected")

    async def pick_file(widget):
        dialog = toga.OpenFileDialog(title="Select token path", multiple_select=False)
        file_path = await navigator.main_window.dialog(dialog)
        if file_path:
            token_label.text = file_path

    async def on_submit(widget):
        result = login(navigator.session, token_label.text, password.value)

        if result.is_ok():
            navigator.navigate("resource_catalog")
            return

        dialog = toga.ErrorDialog(title="Oops", message=result.unwrap_err())
        await navigator.main_window.dialog(dialog)

    return toga.Box(
        children=[
            toga.Label("Login", style=Pack(padding=(0, 0, 10, 0))),
            toga.Button("Select token path", on_press=pick_file),
            token_label,
            password,
            toga.Button("Submit", on_press=on_submit),
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )
