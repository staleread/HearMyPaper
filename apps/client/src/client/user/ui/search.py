import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


def user_search_screen(navigator):
    user_id_input = toga.TextInput(placeholder="Enter User ID", style=Pack(flex=1))

    def on_search(widget):
        user_id = user_id_input.value.strip()
        if user_id:
            navigator.navigate("user_info", user_id)
        else:
            navigator.main_window.info_dialog("Error", "Please enter a User ID")

    def on_back(widget):
        navigator.navigate("resource_catalog")

    container = toga.Box(
        children=[
            toga.Box(
                children=[
                    toga.Label("Search User by ID:", style=Pack(padding=5)),
                    user_id_input,
                ],
                style=Pack(direction=ROW, padding=10),
            ),
            toga.Button(
                "Search",
                on_press=on_search,
                style=Pack(padding=10),
            ),
            toga.Button(
                "Back",
                on_press=on_back,
                style=Pack(padding=10),
            ),
        ],
        style=Pack(direction=COLUMN),
    )

    return container
