import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Any, Callable, cast


def catalog_screen(
    title: str,
    items: list[dict],
    navigator: Any,
    on_item_click: Callable[[dict, Any], None] | None = None,
    actions: list[tuple[str, Callable[[Any], None]]] | None = None,
    parent_catalog: str | None = None,
) -> toga.Box:
    """
    Generic catalog screen similar to file explorer

    Args:
        title: Screen title
        items: List of items with 'id' and 'name' or 'title' fields
        navigator: Navigator instance
        on_item_click: Callback when item is clicked, receives (item, navigator)
        actions: List of action buttons [(label, callback), ...]
        parent_catalog: Optional parent catalog name for back navigation
    """
    children = [
        toga.Label(
            title, style=Pack(font_size=18, font_weight="bold", padding=(0, 0, 10, 0))
        )
    ]

    # Back button if parent catalog is specified
    if parent_catalog:

        def handle_back(widget: toga.Widget) -> None:
            navigator.navigate("resource_catalog")

        back_button = toga.Button(
            f"← Back to {parent_catalog}",
            on_press=cast(Any, handle_back),
            style=Pack(padding=(0, 0, 10, 0)),
        )
        children.append(back_button)

    # Actions row
    if actions:
        action_buttons = []
        for label, callback in actions:

            def handle_action(
                widget: toga.Widget, cb: Callable[[Any], None] = callback
            ) -> None:
                cb(navigator)

            btn = toga.Button(label, on_press=cast(Any, handle_action))
            action_buttons.append(btn)

        actions_box = toga.Box(
            children=action_buttons, style=Pack(direction=ROW, padding=(0, 0, 10, 0))
        )
        children.append(actions_box)

    # Items list
    items_box = toga.Box(style=Pack(direction=COLUMN))

    for item in items:
        item_name = (
            item.get("name")
            or item.get("title")
            or item.get("full_name", f"Item {item['id']}")
        )

        def make_item_handler(item_data):
            return (
                lambda w: on_item_click(item_data, navigator) if on_item_click else None
            )

        item_button = toga.Button(
            f"📁 {item_name}",
            on_press=make_item_handler(item),
            style=Pack(width=300, text_align="left"),
        )
        items_box.add(item_button)

    children.append(items_box)

    return toga.Box(children=children, style=Pack(direction=COLUMN, margin=20, gap=10))
