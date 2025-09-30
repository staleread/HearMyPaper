import toga
from typing import cast, Any
from ..service import get_user_as_response
from ...shared.ui.item_info_screen import item_info_screen


def user_info_screen(navigator, user_id: int):
    """User info screen"""
    result = get_user_as_response(navigator.session, user_id)

    if result.is_err():

        def handle_back(widget: toga.Widget) -> None:
            navigator.navigate("users_catalog")

        return toga.Box(
            children=[
                toga.Label(f"Error loading user: {result.unwrap_err()}"),
                toga.Button("← Back", on_press=cast(Any, handle_back)),
            ],
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
        )

    user_data = result.unwrap()
    # Convert to dict for compatibility with item_info_screen
    user_dict = user_data.model_dump()

    def on_edit_user(item_data, nav):
        nav.navigate("user_edit_form", item_data)

    def on_delete_user(item_data, nav):
        # This should never be called since delete is marked as unsupported
        pass

    def on_export_user(item_data, nav):
        # This should never be called since export is marked as unsupported
        pass

    actions = [
        ("Edit", on_edit_user, True),
        ("Export", on_export_user, False),  # Export not supported (example)
        ("Delete", on_delete_user, False),  # Delete not supported
    ]

    return item_info_screen(
        title=f"User: {user_data.name} {user_data.surname}",
        item_data=user_dict,
        navigator=navigator,
        actions=actions,
        back_target="users_catalog",
    )
