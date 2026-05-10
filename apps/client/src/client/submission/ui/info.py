import asyncio
import toga
from result import Ok
from uuid import UUID
from ...shared.ui.item_info_screen import item_info_screen


def submission_info_screen(navigator, attempt_id):
    if isinstance(attempt_id, str):
        attempt_id = UUID(attempt_id)

    container = toga.Box(children=[toga.Label("Loading attempt details...")])

    async def load_attempt():
        try:
            attempt = await navigator.get_attempt_use_case(attempt_id)

            attempt_data = {
                "id": str(attempt.id),
                "student_id": attempt.student_id,
                "submitted_at": attempt.submitted_at.isoformat(),
                "on_time": "Yes" if attempt.is_on_time else "No",
                "grade": str(attempt.grade)
                if attempt.grade is not None
                else "Not graded",
                "feedback": attempt.feedback or "No feedback",
            }

            def on_grade():
                navigator.navigate("submission_grade_form", attempt_data)

            def on_pdf_to_audio():
                navigator.navigate("submission_convert_form", attempt_id=attempt_id)

            actions = [
                ("Grade", on_grade),
                ("PDF to Audio", on_pdf_to_audio),
            ]

            info_screen = item_info_screen(
                title="Attempt Details",
                data=Ok(attempt_data),
                on_back=lambda w: navigator.navigate("resource_catalog"),
                actions=actions,
            )
            navigator.main_window.content = info_screen
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to load attempt: {e}")
            )
            navigator.navigate("resource_catalog")

    asyncio.create_task(load_attempt())
    return container
