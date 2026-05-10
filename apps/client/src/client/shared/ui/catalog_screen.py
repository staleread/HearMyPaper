import textwrap
import toga
from result import Result, is_err
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from typing import Any


def catalog_screen(
    *,
    title: str,
    headings: list[str],
    data: Result,
    actions: list[tuple[str, Any]] | None = None,
    on_back: Any | None = None,
    on_activate: Any | None = None,
    on_refresh: Any | None = None,
    empty_message: str | None = "No items found.",
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

    empty_label = None
    if empty_message:
        empty_label = toga.Label(
            empty_message,
            style=Pack(text_align="center", margin=(20, 0), font_weight="bold"),
        )

    def update_visibility():
        has_data = len(table.data) > 0
        if empty_label:
            empty_label.style.visibility = "hidden" if has_data else "visible"
        table.style.visibility = "visible" if has_data else "hidden"

    update_visibility()

    def on_row_activate(widget: toga.Table, row: Any, **kwargs: Any):
        if on_activate:
            on_activate(row)

    if on_activate:
        table.on_activate = on_row_activate

    children = [header_box, table]
    if empty_label:
        children.append(empty_label)

    container = toga.Box(
        children=children,
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )

    if on_refresh:

        async def do_refresh():
            new_data = await on_refresh()
            table.data = new_data
            update_visibility()

        import asyncio

        asyncio.create_task(do_refresh())

    return container
