import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from ..service import decrypt_submission


def submission_download_form(navigator, submission_id):
    """
    Форма для завантаження submission-файлу (розшифровка).
    """
    path_input = toga.TextInput(readonly=True)
    choose_button = toga.Button(
        "Choose where to save", on_press=lambda _: choose_path()
    )
    decrypt_button = toga.Button("Decrypt & Save", on_press=lambda _: decrypt_file())

    def choose_path():
        file = toga.FileChooser().save_file()
        if file:
            path_input.value = file[0]

    def decrypt_file():
        encrypted_data = b""  # поки заглушка
        res = decrypt_submission(encrypted_data, path_input.value)
        if res.is_ok():
            navigator.alert("File saved successfully!")
            navigator.navigate("submissions_catalog")
        else:
            navigator.alert(f"Decryption error: {res.err_value}")

    return toga.Box(
        children=[path_input, choose_button, decrypt_button],
        style=Pack(direction=COLUMN, padding=10),
    )
