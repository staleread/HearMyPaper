import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Any, cast


def item_info_screen(
    title: str, item_data: dict, navigator, actions=None, back_target="resource_catalog"
):
    """
    Generic item info screen

    Args:
        title: Screen title
        item_data: Dictionary containing item information
        navigator: Navigator instance
        actions: List of action buttons [(label, callback, supported), ...]
                 where supported is optional boolean (default True)
        back_target: Target screen for back navigation (default: "resource_catalog")
    """
    children = [
        toga.Label(
            title, style=Pack(font_size=18, font_weight="bold", padding=(0, 0, 10, 0))
        )
    ]

    # Actions row
    if actions:
        action_buttons = []
        for action_config in actions:
            if len(action_config) == 2:
                label, callback = action_config
                supported = True
            else:
                label, callback, supported = action_config

            def make_action_handler(cb, is_supported):
                if is_supported:
                    return lambda w: cb(item_data, navigator)
                else:

                    async def show_not_supported():
                        dialog = toga.InfoDialog(
                            title="Not Supported",
                            message=f"'{label}' operation is not supported for this item.",
                        )
                        await navigator.main_window.dialog(dialog)

                    return lambda w: navigator.main_window.app.add_background_task(
                        show_not_supported
                    )

            btn_style = Pack() if supported else Pack(background_color="#cccccc")
            btn = toga.Button(
                label,
                on_press=make_action_handler(callback, supported),
                style=btn_style,
            )
            action_buttons.append(btn)

        actions_box = toga.Box(
            children=action_buttons, style=Pack(direction=ROW, padding=(0, 0, 10, 0))
        )
        children.append(actions_box)

    # Item details
    details_box = toga.Box(style=Pack(direction=COLUMN, gap=5))

    for key, value in item_data.items():
        if key == "id":
            continue  # Skip ID in display

        # Format the key to be more readable
        display_key = key.replace("_", " ").title()

        # Handle different value types
        if isinstance(value, list):
            display_value = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            display_value = str(value)  # Could be improved for nested objects
        else:
            display_value = str(value)

        details_box.add(
            toga.Box(
                children=[
                    toga.Label(
                        f"{display_key}:", style=Pack(font_weight="bold", width=150)
                    ),
                    toga.Label(display_value, style=Pack(flex=1)),
                ],
                style=Pack(direction=ROW, padding=(5, 0)),
            )
        )

    children.append(details_box)

    # Back button
    def handle_back(widget: toga.Widget) -> None:
        navigator.navigate(back_target)

    children.append(
        toga.Button(
            "← Back", on_press=cast(Any, handle_back), style=Pack(padding=(20, 0, 0, 0))
        )
    )

    return toga.Box(children=children, style=Pack(direction=COLUMN, margin=20, gap=10))
