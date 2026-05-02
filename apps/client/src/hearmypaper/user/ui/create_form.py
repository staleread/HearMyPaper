import toga
from datetime import datetime, timedelta

from ...auth.service import create_user_with_credentials
from ...auth.enums import AccessLevel
from ...user.dto import UserCreateDto
from ...shared.ui.components.datetime_picker import DateTimePicker


def user_create_form_screen(navigator):
    credentials_path = None

    async def select_credentials_file():
        dialog = toga.SaveFileDialog(
            title="Select credentials file location",
            suggested_filename="user_credentials.bin",
        )
        file_path = await navigator.main_window.dialog(dialog)
        return str(file_path)

    children = [
        toga.Label(
            "Create New User",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", margin=(0, 0, 10, 0)
            ),
        )
    ]

    name_input = toga.TextInput(placeholder="First Name")
    surname_input = toga.TextInput(placeholder="Last Name")
    email_input = toga.TextInput(placeholder="Email")

    access_level_options = AccessLevel.get_display_options()
    confidentiality_input = toga.Selection(items=access_level_options)
    confidentiality_input.value = AccessLevel.CONFIDENTIAL.to_display_string()

    integrity_checkboxes = {}
    integrity_box = toga.Box(
        style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=(10, 0))
    )

    for level in AccessLevel:
        checkbox = toga.Switch(f"{level.value} - {level.name.title()}")
        if level in [AccessLevel.RESTRICTED, AccessLevel.CONFIDENTIAL]:
            checkbox.value = True
        integrity_checkboxes[level.value] = checkbox
        integrity_box.add(checkbox)

    default_expiry = datetime.now() + timedelta(days=365)
    expires_picker = DateTimePicker(initial_value=default_expiry)

    credentials_label = toga.Label("No credentials file selected")
    password_input = toga.PasswordInput(placeholder="Password for credentials file")

    async def pick_credentials_file(widget):
        nonlocal credentials_path
        file_path = await select_credentials_file()
        if file_path:
            credentials_path = file_path
            credentials_label.text = f"Selected: {file_path}"

    def get_selected_integrity_levels():
        return [
            AccessLevel(level)
            for level, checkbox in integrity_checkboxes.items()
            if checkbox.value
        ]

    async def on_submit(widget):
        if not all([name_input.value, surname_input.value, email_input.value]):
            dialog = toga.ErrorDialog(
                title="Error", message="Please fill in all required fields"
            )
            await navigator.main_window.dialog(dialog)
            return

        if not credentials_path:
            dialog = toga.ErrorDialog(
                title="Error", message="Please select a credentials file location"
            )
            await navigator.main_window.dialog(dialog)
            return

        if not password_input.value:
            dialog = toga.ErrorDialog(
                title="Error",
                message="Please provide a password for the credentials file",
            )
            await navigator.main_window.dialog(dialog)
            return

        integrity_levels = get_selected_integrity_levels()

        try:
            confidentiality_level = AccessLevel.from_display_string(
                confidentiality_input.value
            )

            expires_at = expires_picker.value.isoformat()

            user_dto = UserCreateDto(
                name=name_input.value,
                surname=surname_input.value,
                email=email_input.value,
                confidentiality_level=confidentiality_level,
                integrity_levels=integrity_levels,
                expires_at=expires_at,
                credentials_path=credentials_path,
                credentials_password=password_input.value,
            )

            result = create_user_with_credentials(navigator.session, user_dto)

            if result.is_err():
                dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to create user: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(dialog)
            else:
                result.unwrap()
                dialog = toga.InfoDialog(
                    title="Success", message="User created successfully!"
                )
                await navigator.main_window.dialog(dialog)
                navigator.navigate("users_catalog")

        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Invalid input: {e}")
            await navigator.main_window.dialog(dialog)

    def on_cancel(widget):
        navigator.navigate("users_catalog")

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
            expires_picker.widget,
            toga.Label("Credentials File:"),
            toga.Button("Select Credentials File", on_press=pick_credentials_file),
            credentials_label,
            toga.Label("Password for Credentials File:"),
            password_input,
            toga.Box(
                children=[
                    toga.Button("Create User", on_press=on_submit),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=toga.style.Pack(
                    direction=toga.style.pack.ROW, margin=(10, 0, 0, 0)
                ),
            ),
        ]
    )

    return toga.ScrollContainer(
        horizontal=False,
        content=toga.Box(
            children=children,
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
        ),
    )
