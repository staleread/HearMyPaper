import toga
import asyncio
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from ..service import convert_pdf_to_audio


def pdf_to_audio_form_screen(navigator):
    children = [
        toga.Label(
            "PDF to Audio Converter",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        ),
        toga.Label(
            "Convert your PDF documents to audio files",
            style=Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
        ),
    ]

    pdf_file_input = toga.TextInput(
        placeholder="Path to PDF file", readonly=True, style=Pack(flex=1)
    )

    token_password_input = toga.PasswordInput(
        placeholder="Token password", style=Pack(flex=1)
    )

    output_file_input = toga.TextInput(
        placeholder="Output audio file path",
        readonly=True,
        style=Pack(flex=1),
    )

    async def show_error(message: str):
        dialog = toga.ErrorDialog(title="Error", message=message)
        await navigator.main_window.dialog(dialog)

    async def show_info(message: str):
        dialog = toga.InfoDialog(title="Success", message=message)
        await navigator.main_window.dialog(dialog)

    async def on_select_pdf(widget):
        try:
            file_path = await navigator.main_window.dialog(
                toga.OpenFileDialog(title="Select PDF File", file_types=["pdf"])
            )
            if file_path:
                pdf_file_input.value = str(file_path)
        except Exception as e:
            await show_error(f"File selection error: {e}")

    async def on_select_output(widget):
        try:
            file_path = await navigator.main_window.save_file_dialog(
                title="Save Audio File As",
                suggested_filename="output.mp3",
                file_types=["mp3"],
            )
            if file_path:
                output_file_input.value = str(file_path)
        except Exception as e:
            await show_error(f"File selection error: {e}")

    async def on_convert(widget):
        if not navigator.credentials_path:
            await show_error("Credentials not found. Please login again.")
            navigator.navigate("login")
            return

        if not pdf_file_input.value:
            await show_error("Please select PDF file")
            return

        if not token_password_input.value:
            await show_error("Please enter token password")
            return

        if not output_file_input.value:
            await show_error("Please select output file location")
            return

        try:
            result = convert_pdf_to_audio(
                navigator.session,
                pdf_file_input.value,
                navigator.credentials_path,
                token_password_input.value,
                navigator.app_paths,
            )

            if result.is_ok():
                audio_bytes = result.unwrap()

                # Save audio to file
                with open(output_file_input.value, "wb") as f:
                    f.write(audio_bytes)

                await show_info(
                    f"Audio file saved successfully!\n{output_file_input.value}"
                )
            else:
                await show_error(f"Failed to convert PDF: {result.unwrap_err()}")
        except Exception as e:
            await show_error(f"Conversion error: {e}")

    def on_cancel(widget):
        navigator.navigate("resource_catalog")

    children.extend(
        [
            toga.Label("PDF File:"),
            toga.Box(
                children=[
                    pdf_file_input,
                    toga.Button("Browse", on_press=on_select_pdf),
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            toga.Label("Token Password:"),
            token_password_input,
            toga.Label("Output Audio File:"),
            toga.Box(
                children=[
                    output_file_input,
                    toga.Button("Browse", on_press=on_select_output),
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            toga.Box(
                children=[
                    toga.Button(
                        "Convert", on_press=lambda w: asyncio.create_task(on_convert(w))
                    ),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=Pack(direction=ROW, margin=(20, 0, 0, 0), gap=10),
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
