import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from uuid import UUID


def manage_students_form_screen(navigator, project_id):
    if isinstance(project_id, str):
        project_id = UUID(project_id)

    student_list = toga.Table(
        headings=["Pseudonym"],
        style=Pack(flex=1, height=300),
    )

    new_student_input = toga.TextInput(
        placeholder="Enter student pseudonym", style=Pack(flex=1)
    )

    async def load_students():
        try:
            students = await navigator.manage_students_use_case.get_students(project_id)
            student_list.data = [{"pseudonym": s} for s in students]
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to load students: {e}")
            )

    async def on_add_student(widget):
        pseudonym = new_student_input.value.strip()
        if not pseudonym:
            return

        try:
            await navigator.manage_students_use_case.assign_student(
                project_id, pseudonym
            )
            new_student_input.value = ""
            await load_students()
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to add student: {e}")
            )

    async def on_remove_student(widget):
        selection = student_list.selection
        if selection is None or (isinstance(selection, list) and not selection):
            await navigator.main_window.dialog(
                toga.InfoDialog("Info", "Please select a student to remove")
            )
            return

        row = selection[0] if isinstance(selection, list) else selection
        pseudonym = getattr(row, "pseudonym", None)

        if not pseudonym:
            return

        try:
            await navigator.manage_students_use_case.remove_student(
                project_id, pseudonym
            )
            await load_students()
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to remove student: {e}")
            )

    container = toga.Box(
        children=[
            toga.Label(
                "Manage Project Students",
                style=Pack(font_size=14, font_weight="bold", margin_bottom=10),
            ),
            toga.Box(
                children=[
                    new_student_input,
                    toga.Button("Add", on_press=on_add_student),
                ],
                style=Pack(direction=ROW, gap=5, margin_bottom=10),
            ),
            student_list,
            toga.Box(
                children=[
                    toga.Button("Remove Selected", on_press=on_remove_student),
                    toga.Button(
                        "Back",
                        on_press=lambda w: navigator.navigate(
                            "project_info", project_id
                        ),
                    ),
                ],
                style=Pack(direction=ROW, gap=5, margin_top=10),
            ),
        ],
        style=Pack(direction=COLUMN, margin=20),
    )

    asyncio.create_task(load_students())

    return container
