import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from hearmypaper.services.auth_service import register


def register_screen(navigator):
    username = toga.TextInput(placeholder="Username")
    role = toga.Selection(items=["Student", "Instructor"])

    token_label = toga.Label("No file selected")

    async def pick_file(widget):
        dialog = toga.OpenFileDialog(title="Select token path", multiple_select=False)
        file_path = await navigator.main_window.dialog(dialog)
        if file_path:
            token_label.text = file_path

    async def on_submit(widget):
        register(username.value, role.value, token_label.text)

    return toga.Box(
        children=[
            toga.Label("Register", style=Pack(padding=(0, 0, 10, 0))),
            username,
            role,
            toga.Button("Select token path", on_press=pick_file),
            token_label,
            toga.Button("Submit", on_press=on_submit),
            toga.Button("Back to Login", on_press=lambda w: navigator.navigate("login")),
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )

