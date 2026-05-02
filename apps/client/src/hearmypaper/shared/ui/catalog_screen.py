import textwrap
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
    actions=None,
    on_back=None,
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

    action_buttons = [
        toga.Button(label, on_press=handler) for label, handler in actions or []
    ]
    actions_box = toga.Box(children=action_buttons, style=Pack(direction=ROW))

    header_box = toga.Box(
        children=[back_button, title_label, actions_box],
        style=Pack(direction=ROW, margin=(0, 0, 10, 0), align_items="center"),
    )

    if is_err(data):
        display_error = "\n".join(textwrap.wrap(data.err_value, width=50))

        error_label = toga.Label(
            display_error, style=Pack(color="red", text_align="center", margin=(10, 0))
        )

        return toga.Box(
            children=[header_box, error_label],
            style=Pack(direction=COLUMN, margin=20, gap=10),
        )

    table = toga.Table(
        headings=headings,
        data=data.unwrap(),
        style=Pack(flex=1),
    )

    def on_row_activate(widget: toga.Table, row: Any, **kwargs: Any):
        on_activate(row)

    if on_activate:
        table.on_activate = on_row_activate

    return toga.Box(
        children=[header_box, table], style=Pack(direction=COLUMN, margin=20, gap=10)
    )
