import toga
from result import Result, is_err
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from typing import Any


def catalog_screen(
    *,
    title,
    headings: list[str],
    data: Result,
    on_back,
    actions,
    on_activate=None,
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

    action_buttons = []
    if actions:
        for label, handler in actions:
            btn = toga.Button(label, on_press=handler)
            action_buttons.append(btn)

    actions_box = toga.Box(children=action_buttons, style=Pack(direction=ROW))

    header_box = toga.Box(
        children=[back_button, title_label, actions_box],
        style=Pack(direction=ROW, margin=(0, 0, 10, 0), align_items="center"),
    )

    if is_err(data):
        contents = toga.Label(data.err_value, style=Pack(font_size=14, margin=(10, 0)))
    else:
        table = toga.Table(
            headings=headings,
            data=data.unwrap(),
            style=Pack(flex=1),
        )

        contents = table

        def on_row_activate(widget: toga.Table, row: Any, **kwargs: Any):
            on_activate(row)

        if on_activate:
            table.on_activate = on_row_activate

    return toga.Box(
        children=[header_box, contents], style=Pack(direction=COLUMN, margin=20, gap=10)
    )
