import toga

from ..service import update_user
from ...auth.enums import AccessLevel
from ..dto import UserUpdateDto


def user_edit_form_screen(navigator, user_data):
    children = [
        toga.Label(
            f"Edit User: {user_data.get('name', '')} {user_data.get('surname', '')}",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", margin=(0, 0, 10, 0)
            ),
        )
    ]

    name_input = toga.TextInput(
        value=user_data.get("name", ""), placeholder="First Name"
    )
    surname_input = toga.TextInput(
        value=user_data.get("surname", ""), placeholder="Last Name"
    )
    email_input = toga.TextInput(value=user_data.get("email", ""), placeholder="Email")

    access_level_options = AccessLevel.get_display_options()
    confidentiality_input = toga.Selection(items=access_level_options)
    current_conf_level = AccessLevel(user_data.get("confidentiality_level", 1))
    confidentiality_input.value = current_conf_level.to_display_string()

    integrity_checkboxes = {}
    integrity_box = toga.Box(
        style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=(10, 0))
    )
    current_integrity_levels = user_data.get("integrity_levels", [])

    for level in AccessLevel:
        checkbox = toga.Switch(f"{level.value} - {level.name.title()}")
        checkbox.value = level.value in current_integrity_levels
        integrity_checkboxes[level.value] = checkbox
        integrity_box.add(checkbox)

    expires_input = toga.TextInput(
        value=user_data.get("expires_at", ""), placeholder="Expires At (ISO format)"
    )

    def get_selected_integrity_levels():
        return [
            level for level, checkbox in integrity_checkboxes.items() if checkbox.value
        ]

    async def on_submit(widget):
        if not all([name_input.value, surname_input.value, email_input.value]):
            dialog = toga.ErrorDialog(
                title="Error", message="Please fill in all required fields"
            )
            await navigator.main_window.dialog(dialog)
            return

        integrity_levels = get_selected_integrity_levels()

        try:
            confidentiality_level = AccessLevel.from_display_string(
                str(confidentiality_input.value)
            )

            integrity_access_levels = [AccessLevel(level) for level in integrity_levels]

            dto = UserUpdateDto(
                name=name_input.value,
                surname=surname_input.value,
                email=email_input.value,
                confidentiality_level=confidentiality_level,
                integrity_levels=integrity_access_levels,
                expires_at=expires_input.value,
            )

            result = update_user(navigator.session, user_data["id"], dto)

            if result.is_err():
                dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to update user: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(dialog)
            else:
                result.unwrap()
                success_dialog = toga.InfoDialog(
                    title="Success", message="User updated successfully!"
                )
                await navigator.main_window.dialog(success_dialog)
                navigator.navigate("user_info", user_data["id"])

        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Invalid input: {e}")
            await navigator.main_window.dialog(dialog)

    def on_cancel(widget):
        navigator.navigate("user_info", user_data["id"])

    children.extend(
        [
            toga.Label("First Name:"),
            name_input,
            toga.Label("Last Name:"),
            surname_input,
            toga.Label("Email:"),
            email_input,
            toga.Label("Confidentiality Level:"),
            toga.Label(
                "(Maximum level user can read)",
                style=toga.style.Pack(font_size=10, color="#666666"),
            ),
            confidentiality_input,
            toga.Label("Integrity Levels (optional):"),
            toga.Label(
                "(Levels user can write to - none selected means no write access)",
                style=toga.style.Pack(font_size=10, color="#666666"),
            ),
            integrity_box,
            toga.Label("Expires At:"),
            expires_input,
            toga.Box(
                children=[
                    toga.Button("Update User", on_press=on_submit),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=toga.style.Pack(
                    direction=toga.style.pack.ROW, margin=(10, 0, 0, 0)
                ),
            ),
        ]
    )

    return toga.ScrollContainer(
        content=toga.Box(
            children=children,
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
        )
    )
