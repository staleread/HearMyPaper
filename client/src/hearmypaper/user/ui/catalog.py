import toga
from ..api import get_users
from ...shared.ui.catalog_screen import catalog_screen


def users_catalog_screen(navigator):
    """Users catalog screen"""
    result = get_users(navigator.session)

    if result.is_err():
        return toga.Box(
            children=[
                toga.Label(f"Error loading users: {result.unwrap_err()}"),
                toga.Button(
                    "← Back", on_press=lambda w: navigator.navigate("resource_catalog")
                ),
            ],
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
        )

    users = result.unwrap()
    # Convert to dict list for compatibility with catalog_screen
    users_dict = [user.model_dump() for user in users]

    def on_user_click(user, nav):
        nav.navigate_with_data("user_info", user["id"])

    def on_create_user(nav):
        nav.navigate("user_create_form")

    actions = [("Create User", on_create_user)]

    return catalog_screen(
        title="Users",
        items=users_dict,
        navigator=navigator,
        on_item_click=on_user_click,
        actions=actions,
        parent_catalog="Resources",
    )
