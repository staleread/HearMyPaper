import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Any, Callable, cast
from collections.abc import Awaitable


def form_screen(
    title: str,
    fields: list[dict],
    navigator: Any,
    on_submit: Callable[[dict, Any], Awaitable[None]],
    on_cancel: Callable[[Any], None],
) -> toga.ScrollContainer:
    """
    Simple form screen component

    Args:
        title: Form title
        fields: List of field definitions with 'name', 'label', 'type', 'value'
        navigator: Navigator instance
        on_submit: Callback for form submission (receives form_data and navigator)
        on_cancel: Callback for cancel action (receives navigator)
    """

    widgets = {}
    form_widgets = []

    # Create form fields
    for field in fields:
        label = toga.Label(field["label"], style=Pack(padding=(5, 0)))

        if field["type"] == "text":
            widget = toga.TextInput(value=field.get("value", ""), style=Pack(flex=1))
        elif field["type"] == "multiline":
            widget = toga.MultilineTextInput(
                value=field.get("value", ""), style=Pack(flex=1, height=100)
            )
        elif field["type"] == "number":
            widget = toga.NumberInput(value=field.get("value", 0), style=Pack(flex=1))
        elif field["type"] == "email":
            widget = toga.TextInput(value=field.get("value", ""), style=Pack(flex=1))
        else:
            widget = toga.TextInput(value=field.get("value", ""), style=Pack(flex=1))

        widgets[field["name"]] = widget

        field_box = toga.Box(
            children=[label, widget], style=Pack(direction=COLUMN, padding=5)
        )
        form_widgets.append(field_box)

    def get_form_data():
        """Extract form data from widgets"""
        return {name: widget.value for name, widget in widgets.items()}

    async def handle_submit(widget: toga.Widget) -> None:
        """Handle form submission"""
        form_data = get_form_data()
        await on_submit(form_data, navigator)

    def handle_cancel(widget: toga.Widget) -> None:
        """Handle form cancellation"""
        on_cancel(navigator)

    # Create buttons
    submit_button = toga.Button(
        "Submit", on_press=cast(Any, handle_submit), style=Pack(flex=1, padding=5)
    )
    cancel_button = toga.Button(
        "Cancel", on_press=cast(Any, handle_cancel), style=Pack(flex=1, padding=5)
    )

    button_box = toga.Box(
        children=[cancel_button, submit_button], style=Pack(direction=ROW, padding=10)
    )

    # Create main container
    main_box = toga.Box(
        children=[
            toga.Label(
                title, style=Pack(text_align="center", font_size=16, padding=10)
            ),
            *form_widgets,
            button_box,
        ],
        style=Pack(direction=COLUMN, padding=20),
    )

    return toga.ScrollContainer(content=main_box)
