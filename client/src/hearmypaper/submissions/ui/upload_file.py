import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from ..api import get_instructor_key, create_submission, create_project_student_api
from ..service import encrypt_submission
from ..dto import SubmissionCreateRequest


def submission_upload_form(navigator, project_student_id: int | None = None):
    title_input = toga.TextInput(placeholder="Title")
    description_input = toga.TextInput(placeholder="Description")
    file_input = toga.TextInput(readonly=True)

    # --- Зберігаємо поточний project ID ---
    current_project_id = project_student_id

    async def show_error(message: str):
        dialog = toga.ErrorDialog(title="Error", message=message)
        await navigator.main_window.dialog(dialog)

    async def show_info(message: str):
        dialog = toga.InfoDialog(title="Success", message=message)
        await navigator.main_window.dialog(dialog)

    async def choose_file_async(widget):
        dialog = toga.OpenFileDialog(title="Select a file")
        result = await widget.app.main_window.dialog(dialog)
        if result:
            file_input.value = str(result)

    def choose_file(widget):
        asyncio.create_task(choose_file_async(widget))

    def handle_submit(widget=None):
        nonlocal current_project_id

        async def submit_async():
            nonlocal current_project_id

            # Створюємо проект студента, якщо немає
            if current_project_id is None:
                res = create_project_student_api(navigator.session)
                if res.is_err():
                    await show_error(f"Failed to create project: {res.err_value}")
                    return
                current_project_id = res.unwrap()["project_student_id"]

            if not title_input.value.strip():
                await show_error("Title is required!")
                return

            if not file_input.value:
                await show_error("Please choose a file to submit!")
                return

            # Отримуємо ключ інструктора
            key_res = get_instructor_key(navigator.session, current_project_id)
            if key_res.is_err():
                await show_error(f"Failed to get public key: {key_res.err_value}")
                return

            # Шифруємо файл
            enc_res = encrypt_submission(file_input.value, key_res.unwrap())
            if enc_res.is_err():
                await show_error(f"Encryption failed: {enc_res.err_value}")
                return

            # Створюємо запит
            req = SubmissionCreateRequest(
                project_student_id=current_project_id,
                title=title_input.value,
                encrypted_content=enc_res.unwrap(),
            )

            result = create_submission(navigator.session, req)
            if result.is_ok():
                await show_info("Submission uploaded successfully!")
                navigator.navigate("submissions_catalog")
            else:
                await show_error(f"Upload failed: {result.err_value}")

        asyncio.create_task(submit_async())

    choose_button = toga.Button("Choose File", on_press=choose_file)
    submit_button = toga.Button("Submit", on_press=handle_submit)

    return toga.Box(
        children=[
            title_input,
            description_input,
            file_input,
            choose_button,
            submit_button,
        ],
        style=Pack(direction=COLUMN, margin=10),
    )
