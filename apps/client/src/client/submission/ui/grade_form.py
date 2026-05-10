import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from uuid import UUID


def submission_grade_form_screen(navigator, attempt_data):
    attempt_id = UUID(attempt_data["id"])

    grade_input = toga.NumberInput(
        min=0,
        max=100,
        value=int(attempt_data.get("grade", 0))
        if attempt_data.get("grade") != "Not graded"
        else 0,
    )
    feedback_input = toga.MultilineTextInput(
        value=attempt_data.get("feedback", "")
        if attempt_data.get("feedback") != "No feedback"
        else "",
        placeholder="Instructor Feedback",
        style=Pack(height=150),
    )

    async def on_submit(widget):
        try:
            grade_val = grade_input.value
            if grade_val is None:
                raise ValueError("Grade is required")

            await navigator.grade_attempt_use_case(
                attempt_id=attempt_id,
                grade=int(grade_val),
                feedback=feedback_input.value.strip() or None,
            )
            await navigator.main_window.dialog(
                toga.InfoDialog("Success", "Attempt graded successfully")
            )
            navigator.navigate("submission_info", attempt_id)
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to grade attempt: {e}")
            )

    def on_cancel(widget):
        navigator.navigate("submission_info", attempt_id)

    container = toga.Box(
        children=[
            toga.Label(
                f"Grade Attempt: {attempt_id}",
                style=Pack(font_size=14, font_weight="bold", margin_bottom=10),
            ),
            toga.Label(f"Student: {attempt_data['student_id']}"),
            toga.Label("Grade (0-100):"),
            grade_input,
            toga.Label("Feedback:"),
            feedback_input,
            toga.Box(
                children=[
                    toga.Button("Submit Grade", on_press=on_submit),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=Pack(direction=ROW, margin=(10, 0, 0, 0), gap=10),
            ),
        ],
        style=Pack(direction=COLUMN, margin=20, gap=10),
    )

    return toga.ScrollContainer(horizontal=False, content=container)
