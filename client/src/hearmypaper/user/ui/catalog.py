from hearmypaper.shared.ui.catalog_screen import catalog_screen

from ..service import get_users_list


def users_catalog_screen(navigator):
    def on_row_activate(row):
        navigator.navigate("user_info", row.id)

    data = (
        get_users_list(navigator.session)
        .map(lambda users: [user.model_dump() for user in users])
        .map_err(lambda err: f"Error loading users: {err}")
    )

    actions = [("Create User", lambda w: navigator.navigate("user_create_form"))]

    return catalog_screen(
        title="Users",
        headings=["Full name"],
        data=data,
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=actions,
        on_activate=on_row_activate,
    )
