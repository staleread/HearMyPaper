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
            if not attempt:
                await navigator.main_window.dialog(
                    toga.ErrorDialog("Error", "Attempt not found")
                )
                navigator.navigate("resource_catalog")
                return

            attempt_data = {
                "id": str(attempt.id),
                "project_id": str(attempt.project_id),
                "student_id": attempt.student_id,
                "submitted_at": attempt.submitted_at.isoformat(),
                "on_time": "Yes" if attempt.is_on_time else "No",
                "grade": str(attempt.grade)
                if attempt.grade is not None
                else "Not graded",
                "feedback": attempt.feedback or "No feedback",
            }

            def on_grade(w):
                navigator.navigate("submission_grade_form", attempt_data)

            async def on_pdf_to_audio(w):
                try:
                    file_path = await navigator.main_window.open_file_dialog(
                        title="Select PDF to Convert",
                        file_types=["pdf"],
                    )
                    if not file_path:
                        return

                    await navigator.request_attempt_conversion_use_case(
                        attempt_id, str(file_path)
                    )
                    await navigator.main_window.dialog(
                        toga.InfoDialog("Success", "Conversion requested successfully")
                    )
                    navigator.navigate("conversions_catalog")
                except Exception as e:
                    await navigator.main_window.dialog(
                        toga.ErrorDialog("Error", f"Failed to request conversion: {e}")
                    )

            async def on_download():
                navigator.navigate("submission_unseal_form", attempt_id=attempt_id)

            actions = [
                ("Download", lambda w: asyncio.create_task(on_download())),
                ("Grade", on_grade),
                ("PDF to Audio", lambda w: asyncio.create_task(on_pdf_to_audio(w))),
            ]

            info_screen = item_info_screen(
                title="Attempt Details",
                data=Ok(attempt_data),
                on_back=lambda w: navigator.navigate(
                    "submissions_catalog", attempt.project_id
                ),
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
