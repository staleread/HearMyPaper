import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from ..service import login


def login_screen(navigator):
    title_label = toga.Label(
        "Login", style=Pack(font_size=14, font_weight="bold", flex=1)
    )

    header_box = toga.Box(
        children=[title_label],
        style=Pack(margin=(0, 0, 10, 0)),
    )

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
            header_box,
            toga.Button("Select token path", on_press=pick_file),
            token_label,
            password,
            toga.Button("Submit", on_press=on_submit),
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )
