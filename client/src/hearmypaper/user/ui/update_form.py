import toga
from typing import Any, cast
from ..service import update_user_with_dto
from ...auth.enums import AccessLevel
from ..dto import UserUpdateDto


def user_edit_form_screen(navigator, user_data: dict):
    """User edit form screen"""

    # Custom form
    children = [
        toga.Label(
            f"Edit User: {user_data.get('name', '')} {user_data.get('surname', '')}",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", padding=(0, 0, 10, 0)
            ),
        )
    ]

    # Form inputs with current values
    name_input = toga.TextInput(
        value=user_data.get("name", ""), placeholder="First Name"
    )
    surname_input = toga.TextInput(
        value=user_data.get("surname", ""), placeholder="Last Name"
    )
    email_input = toga.TextInput(value=user_data.get("email", ""), placeholder="Email")

    # Confidentiality level dropdown
    access_level_options = AccessLevel.get_display_options()
    confidentiality_input = toga.Selection(items=access_level_options)
    current_conf_level = AccessLevel(user_data.get("confidentiality_level", 1))
    confidentiality_input.value = current_conf_level.to_display_string()

    # Integrity levels as checkboxes
    integrity_checkboxes = {}
    integrity_box = toga.Box(
        style=toga.style.Pack(direction=toga.style.pack.COLUMN, padding=(10, 0))
    )
    current_integrity_levels = user_data.get("integrity_levels", [])

    for level in AccessLevel:
        checkbox = toga.Switch(f"{level.value} - {level.name.title()}")
        # Set checkbox state based on current user data
        checkbox.value = level.value in current_integrity_levels
        integrity_checkboxes[level.value] = checkbox
        integrity_box.add(checkbox)

    expires_input = toga.TextInput(
        value=user_data.get("expires_at", ""), placeholder="Expires At (ISO format)"
    )

    def get_selected_integrity_levels() -> list[int]:
        """Get list of selected integrity levels"""
        return [
            level for level, checkbox in integrity_checkboxes.items() if checkbox.value
        ]

    async def on_submit(widget: toga.Widget) -> None:
        # Validate inputs
        if not all([name_input.value, surname_input.value, email_input.value]):
            dialog = toga.ErrorDialog(
                title="Error", message="Please fill in all required fields"
            )
            await navigator.main_window.dialog(dialog)
            return

        # Get integrity levels (empty selection is allowed)
        integrity_levels = get_selected_integrity_levels()

        try:
            # Parse confidentiality level
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

            result = update_user_with_dto(navigator.session, user_data["id"], dto)

            if result.is_err():
                dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to update user: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(dialog)
            else:
                result.unwrap()  # Ensure result is consumed
                success_dialog = toga.InfoDialog(
                    title="Success", message="User updated successfully!"
                )
                await navigator.main_window.dialog(success_dialog)
                navigator.navigate_with_data("user_info", user_data["id"])

        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Invalid input: {e}")
            await navigator.main_window.dialog(dialog)

    def on_cancel(widget: toga.Widget) -> None:
        navigator.navigate_with_data("user_info", user_data["id"])

    # Build form
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
                    toga.Button("Update User", on_press=cast(Any, on_submit)),
                    toga.Button("Cancel", on_press=cast(Any, on_cancel)),
                ],
                style=toga.style.Pack(
                    direction=toga.style.pack.ROW, padding=(10, 0, 0, 0)
                ),
            ),
        ]
    )

    return toga.Box(
        children=children,
        style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
    )
