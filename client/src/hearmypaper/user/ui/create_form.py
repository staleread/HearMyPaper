import toga
from datetime import datetime, timedelta
from ...auth.service import create_user_with_credentials
from ...auth.enums import AccessLevel
from ...auth.dto import UserCreateDto


def user_create_form_screen(navigator):
    """User creation form screen with key generation and credential storage"""

    # State variables
    credentials_path = None

    async def select_credentials_file():
        """Select file for saving user credentials"""
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
                font_size=18, font_weight="bold", padding=(0, 0, 10, 0)
            ),
        )
    ]

    # Form inputs
    name_input = toga.TextInput(placeholder="First Name")
    surname_input = toga.TextInput(placeholder="Last Name")
    email_input = toga.TextInput(placeholder="Email")

    # Access level dropdowns with descriptive text
    access_level_options = AccessLevel.get_display_options()
    confidentiality_input = toga.Selection(items=access_level_options)
    confidentiality_input.value = (
        AccessLevel.CONFIDENTIAL.to_display_string()
    )  # Default to CONFIDENTIAL

    # Integrity levels as checkboxes
    integrity_checkboxes = {}
    integrity_box = toga.Box(
        style=toga.style.Pack(direction=toga.style.pack.COLUMN, padding=(10, 0))
    )

    for level in AccessLevel:
        checkbox = toga.Switch(f"{level.value} - {level.name.title()}")
        # Default to RESTRICTED and CONFIDENTIAL for admin users
        if level in [AccessLevel.RESTRICTED, AccessLevel.CONFIDENTIAL]:
            checkbox.value = True
        integrity_checkboxes[level.value] = checkbox
        integrity_box.add(checkbox)

    expires_input = toga.TextInput(
        placeholder="Expires At (ISO format, leave empty for 1 year)"
    )

    credentials_label = toga.Label("No credentials file selected")
    password_input = toga.PasswordInput(placeholder="Password for credentials file")

    async def pick_credentials_file(widget):
        nonlocal credentials_path
        file_path = await select_credentials_file()
        if file_path:
            credentials_path = file_path
            credentials_label.text = f"Selected: {file_path}"

    def get_selected_integrity_levels() -> list[AccessLevel]:
        """Get list of selected integrity levels"""
        return [
            AccessLevel(level)
            for level, checkbox in integrity_checkboxes.items()
            if checkbox.value
        ]

    async def on_submit(widget):
        # Validate inputs
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

        # Check if at least one integrity level is selected
        integrity_levels = get_selected_integrity_levels()
        if not integrity_levels:
            dialog = toga.ErrorDialog(
                title="Error", message="Please select at least one integrity level"
            )
            await navigator.main_window.dialog(dialog)
            return

        try:
            # Parse confidentiality level
            confidentiality_level = AccessLevel.from_display_string(
                confidentiality_input.value
            )

            # Set default expiry if not provided
            expires_at = expires_input.value
            if not expires_at:
                default_expiry = (datetime.now() + timedelta(days=365)).isoformat()
                expires_at = default_expiry

            # Create DTO
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

            # Create user with generated credentials
            result = create_user_with_credentials(navigator.session, user_dto)

            if result.is_err():
                dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to create user: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(dialog)
            else:
                result.unwrap()  # Ensure result is consumed
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

    # Build form manually for custom file selection
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
            toga.Label("Integrity Levels:"),
            toga.Label(
                "(Levels user can write to)",
                style=toga.style.Pack(font_size=10, color="#666666"),
            ),
            integrity_box,
            toga.Label("Expires At (optional):"),
            expires_input,
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
                    direction=toga.style.pack.ROW, padding=(10, 0, 0, 0)
                ),
            ),
        ]
    )

    return toga.Box(
        children=children,
        style=toga.style.Pack(direction=toga.style.pack.COLUMN, margin=20, gap=10),
    )
