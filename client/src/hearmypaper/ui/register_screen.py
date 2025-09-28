import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from hearmypaper.services.auth_service import register


def register_screen(navigator):
    username = toga.TextInput(placeholder="Username")
    role = toga.Selection(items=["Student", "Instructor", "Curator"])
    password = toga.PasswordInput(placeholder="Password")

    token_label = toga.Label("No file selected")

    async def pick_file(widget):
        dialog = toga.SaveFileDialog(
            title="Select token path", suggested_filename="hearmypaper_token.bin"
        )
        file_path = await navigator.main_window.dialog(dialog)
        if file_path:
            token_label.text = file_path

    async def on_submit(widget):
        error = register(username.value, role.value, token_label.text, password.value)

        if not error:
            navigator.navigate("login")
            dialog = toga.InfoDialog(title="Info", message="Registration successful")

            return await navigator.main_window.dialog(dialog)

        dialog = toga.ErrorDialog(title="Oops", message=error)
        await navigator.main_window.dialog(dialog)

    return toga.Box(
        children=[
            toga.Label("Register", style=Pack(padding=(0, 0, 10, 0))),
            username,
            role,
            toga.Button("Select token path", on_press=pick_file),
            token_label,
            password,
            toga.Button("Submit", on_press=on_submit),
            toga.Button(
                "Back to Login", on_press=lambda w: navigator.navigate("login")
            ),
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )
