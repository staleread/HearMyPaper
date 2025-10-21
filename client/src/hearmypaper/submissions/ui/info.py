import toga
from toga.style import Pack
from toga.style.pack import COLUMN


def submission_info_screen(navigator, submission_id):
    """
    Показує деталі submission (можна розширити пізніше).
    """
    return toga.Box(
        children=[
            toga.Label(f"Submission ID: {submission_id}"),
            toga.Button(
                "Download",
                on_press=lambda _: navigator.navigate(
                    "submission_download_form", submission_id=submission_id
                ),
            ),
            toga.Button(
                "Back", on_press=lambda _: navigator.navigate("submissions_catalog")
            ),
        ],
        style=Pack(direction=COLUMN, padding=10),
    )
