import toga
from result import Result, is_err
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def item_info_screen(
    *,
    title,
    data: Result,
    actions=None,
    on_back=None,
):
    back_button = toga.Button(
        "<",
        on_press=on_back,
        enabled=on_back is not None,
        style=Pack(width=35, height=35, font_weight="bold"),
    )

    title_label = toga.Label(
        title, style=Pack(font_size=14, font_weight="bold", flex=1, margin_left=10)
    )

    action_buttons = (
        [
            toga.Button(label, on_press=lambda widget, **kwargs: handler())
            for label, handler in actions
        ]
        if actions
        else []
    )
    actions_box = toga.Box(children=action_buttons, style=Pack(direction=ROW))

    header_box = toga.Box(
        children=[back_button, title_label, actions_box],
        style=Pack(direction=ROW, margin=(0, 0, 10, 0), align_items="center"),
    )

    if is_err(data):
        print("ERROR HERE")
        error_label = toga.Label(
            data.err_value, style=Pack(color="red", font_size=14, margin=(10, 0))
        )
        return toga.Box(
            children=[header_box, error_label],
            style=Pack(direction=COLUMN, margin=20, gap=10),
        )

    item_data = data.unwrap()
    details_box = toga.Box(style=Pack(direction=COLUMN, gap=5))

    for key, value in item_data.items():
        if key.endswith("id"):
            continue

        display_key = key.replace("_", " ").title()

        if isinstance(value, list):
            display_value = ", ".join(str(v) for v in value)
        else:
            display_value = str(value)

        value_label = toga.Label(display_value, style=Pack(flex=1, text_align="left"))

        details_box.add(
            toga.Box(
                children=[
                    toga.Label(
                        f"{display_key}:", style=Pack(font_weight="bold", width=150)
                    ),
                    value_label,
                ],
                style=Pack(direction=ROW, margin=(5, 0)),
            )
        )

    return toga.ScrollContainer(
        content=toga.Box(
            children=[header_box, details_box],
            style=Pack(direction=COLUMN, margin=20, gap=10),
        )
    )
