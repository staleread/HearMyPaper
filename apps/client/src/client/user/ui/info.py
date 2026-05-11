import asyncio
import toga
from toga.style import Pack
from toga.constants import COLUMN
from result import Ok
from ...shared.ui.item_info_screen import item_info_screen


def user_info_screen(navigator, user_id):
    container = toga.Box(children=[toga.Label("Loading user details...")])

    async def load_user():
        try:
            user = await navigator.get_user_use_case(user_id)

            if user is None:
                # Remove the "Loading" label
                for child in list(container.children):
                    container.remove(child)

                # Add the Not Found message
                container.add(
                    toga.Box(
                        children=[
                            toga.Label(
                                f"User with ID '{user_id}' not found.",
                                style=Pack(padding=20, font_weight="bold"),
                            ),
                            toga.Button(
                                "Back to Search",
                                on_press=lambda w: navigator.navigate("user_search"),
                                style=Pack(padding=10),
                            ),
                        ],
                        style=Pack(direction=COLUMN, align_items="center", flex=1),
                    )
                )
                return

            user_data = {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "confidentiality_level": user.confidentiality_level.value,
                "integrity_levels": [level.value for level in user.integrity_levels],
                "created_at": user.created_at.isoformat(),
            }

            def on_edit_user(w):
                navigator.navigate("user_edit_form", user_data)

            actions = [("Edit", on_edit_user)]

            info_screen = item_info_screen(
                title="User Details",
                data=Ok(user_data),
                on_back=lambda w: navigator.navigate("user_search"),
                actions=actions,
            )
            navigator.main_window.content = info_screen
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to load user: {e}")
            )
            navigator.navigate("user_search")

    asyncio.create_task(load_user())
    return container
