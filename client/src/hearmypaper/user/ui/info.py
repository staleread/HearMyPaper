from hearmypaper.shared.ui.item_info_screen import item_info_screen
from ..service import get_user


def user_info_screen(navigator, user_id):
    data = get_user(navigator.session, user_id).map(lambda user: user.model_dump())

    def on_edit_user():
        if data.is_ok():
            navigator.navigate("user_edit_form", data.unwrap())

    actions = [("Edit", on_edit_user)]

    return item_info_screen(
        title="User Details",
        data=data,
        on_back=lambda w: navigator.navigate("users_catalog"),
        actions=actions,
    )
