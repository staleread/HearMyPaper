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

    back_button = toga.Button(
        "<",
        on_press=on_back,
        style=Pack(width=35, height=35, font_weight="bold"),
    )

    title_label = toga.Label(
        "User Search",
        style=Pack(font_size=14, font_weight="bold", flex=1, margin_left=10),
    )

    header_box = toga.Box(
        children=[back_button, title_label],
        style=Pack(direction=ROW, margin=(0, 0, 10, 0), align_items="center"),
    )

    container = toga.Box(
        children=[
            header_box,
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
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )

    return container
