import toga

from ..service import assign_students, get_project_students
from ..dto import StudentAssignmentDto


def manage_students_form_screen(navigator, project_id):
    children = [
        toga.Label(
            "Manage Students",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", margin=(0, 0, 10, 0)
            ),
        ),
        toga.Label(
            "Enter student emails, one per line:",
            style=toga.style.Pack(margin=(0, 0, 5, 0)),
        ),
    ]

    # Fetch existing student emails
    existing_emails_result = get_project_students(navigator.session, project_id)
    initial_value = ""
    if existing_emails_result.is_ok():
        existing_emails = existing_emails_result.unwrap()
        initial_value = "\n".join(existing_emails)

    emails_input = toga.MultilineTextInput(
        placeholder="student1@example.com\nstudent2@example.com",
        value=initial_value,
        style=toga.style.Pack(height=200),
    )

    async def on_submit(widget):
        if not emails_input.value or not emails_input.value.strip():
            dialog = toga.ErrorDialog(
                title="Error", message="Please enter at least one email address"
            )
            await navigator.main_window.dialog(dialog)
            return

        email_lines = [
            line.strip()
            for line in emails_input.value.strip().split("\n")
            if line.strip()
        ]

        invalid_emails = [
            email for email in email_lines if "@" not in email or "." not in email
        ]
        if invalid_emails:
            dialog = toga.ErrorDialog(
                title="Error",
                message=f"Invalid email addresses:\n{', '.join(invalid_emails)}",
            )
            await navigator.main_window.dialog(dialog)
            return

        assignment_dto = StudentAssignmentDto(student_emails=email_lines)

        try:
            result = assign_students(navigator.session, project_id, assignment_dto)

            if result.is_ok():
                success_dialog = toga.InfoDialog(
                    title="Success",
                    message="Students assigned successfully!",
                )
                await navigator.main_window.dialog(success_dialog)
                navigator.navigate("project_info", project_id)
            else:
                error_dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to assign students: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(error_dialog)
        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Invalid input: {e}")
            await navigator.main_window.dialog(dialog)

    def on_cancel(widget):
        navigator.navigate("project_info", project_id)

    children.extend(
        [
            emails_input,
            toga.Box(
                children=[
                    toga.Button("Save", on_press=on_submit),
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
