import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from client_core.models import AccessLevel


def user_create_form_screen(navigator):
    credentials_path = None

    async def select_credentials_file():
        dialog = toga.SaveFileDialog(
            title="Select credentials file location",
            suggested_filename="user_credentials.bin",
        )
        file_path = await navigator.main_window.dialog(dialog)
        return str(file_path) if file_path else None

    children = [
        toga.Label(
            "Create New User",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        )
    ]

    name_input = toga.TextInput(placeholder="First Name")
    surname_input = toga.TextInput(placeholder="Last Name")
    email_input = toga.TextInput(placeholder="Email")

    access_level_options = [level.value for level in AccessLevel]
    confidentiality_input = toga.Selection(items=access_level_options)
    confidentiality_input.value = AccessLevel.CONFIDENTIAL.value

    integrity_checkboxes = {}
    integrity_box = toga.Box(style=Pack(direction=COLUMN, margin=(10, 0)))

    for level in AccessLevel:
        checkbox = toga.Switch(level.value)
        if level in [AccessLevel.RESTRICTED, AccessLevel.CONFIDENTIAL]:
            checkbox.value = True
        integrity_checkboxes[level] = checkbox
        integrity_box.add(checkbox)

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

        if not credentials_path:
            await navigator.main_window.dialog(
                toga.ErrorDialog(
                    title="Error", message="Please select a credentials file location"
                )
            )
            return

        if not password_input.value:
            await navigator.main_window.dialog(
                toga.ErrorDialog(
                    title="Error",
                    message="Please provide a password for the credentials file",
                )
            )
            return

        try:
            confidentiality_level = AccessLevel(str(confidentiality_input.value))
            integrity_levels = get_selected_integrity_levels()

            user = await navigator.create_user_use_case(
                name=name_input.value,
                surname=surname_input.value,
                email=email_input.value,
                confidentiality_level=confidentiality_level,
                integrity_levels=integrity_levels,
                credentials_path=credentials_path,
                credentials_password=password_input.value,
            )

            await navigator.main_window.dialog(
                toga.InfoDialog(
                    title="Success",
                    message=f"User created successfully! ID: {user.id}",
                )
            )
            navigator.credentials_path = credentials_path
            navigator.navigate("user_info", user.id)

        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog(title="Error", message=f"Failed to create user: {e}")
            )

    def on_cancel(widget):
        navigator.navigate("user_search")

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
