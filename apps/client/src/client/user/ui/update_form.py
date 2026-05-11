import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from client_core.models import AccessLevel


def user_edit_form_screen(navigator, user_data):
    children = [
        toga.Label(
            "Edit User",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        )
    ]

    name_input = toga.TextInput(
        value=user_data.get("name", ""), placeholder="First Name"
    )
    surname_input = toga.TextInput(
        value=user_data.get("surname", ""), placeholder="Last Name"
    )
    email_input = toga.TextInput(value=user_data.get("email", ""), placeholder="Email")

    access_level_options = [level.value for level in AccessLevel]
    confidentiality_input = toga.Selection(items=access_level_options)
    confidentiality_input.value = user_data.get("confidentiality_level")

    integrity_checkboxes = {}
    integrity_box = toga.Box(style=Pack(direction=COLUMN, margin=(10, 0)))
    current_integrity_levels = user_data.get("integrity_levels", [])

    for level in AccessLevel:
        checkbox = toga.Switch(level.value)
        checkbox.value = level.value in current_integrity_levels
        integrity_checkboxes[level] = checkbox
        integrity_box.add(checkbox)

    def get_selected_integrity_levels():
        return [
            level for level, checkbox in integrity_checkboxes.items() if checkbox.value
        ]

    async def on_submit(widget):
        if not all([name_input.value, surname_input.value, email_input.value]):
            await navigator.main_window.dialog(
                toga.ErrorDialog(
                    title="Error", message="Please fill in all required fields"
                )
            )
            return

        try:
            confidentiality_level = AccessLevel(str(confidentiality_input.value))
            integrity_levels = get_selected_integrity_levels()

            await navigator.update_user_use_case(
                user_id=user_data["id"],
                name=name_input.value,
                surname=surname_input.value,
                email=email_input.value,
                confidentiality_level=confidentiality_level,
                integrity_levels=integrity_levels,
            )

            await navigator.main_window.dialog(
                toga.InfoDialog(title="Success", message="User updated successfully!")
            )
            navigator.navigate("user_info", user_data["id"])

        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog(title="Error", message=f"Failed to update user: {e}")
            )

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
                style=Pack(font_size=10, color="#666666"),
            ),
            confidentiality_input,
            toga.Label("Integrity Levels (optional):"),
            toga.Label(
                "(Levels user can write to - none selected means no write access)",
                style=Pack(font_size=10, color="#666666"),
            ),
            integrity_box,
            toga.Box(
                children=[
                    toga.Button("Update User", on_press=on_submit),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=Pack(direction=ROW, margin=(10, 0, 0, 0), gap=10),
            ),
        ]
    )

    return toga.ScrollContainer(
        horizontal=False,
        content=toga.Box(
            children=children,
            style=Pack(direction=COLUMN, margin=20, gap=10),
        ),
    )
