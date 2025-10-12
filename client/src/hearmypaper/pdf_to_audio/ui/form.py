import toga

from ..service import convert_pdf_to_audio


def pdf_to_audio_form_screen(navigator):
    children = [
        toga.Label(
            "PDF to Audio Converter",
            style=toga.style.Pack(
                font_size=18, font_weight="bold", margin=(0, 0, 10, 0)
            ),
        ),
        toga.Label(
            "Convert your PDF documents to audio files",
            style=toga.style.Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
        ),
    ]

    pdf_file_input = toga.TextInput(
        placeholder="Path to PDF file", readonly=True, style=toga.style.Pack(flex=1)
    )

    token_path_input = toga.TextInput(
        placeholder="Path to credentials token file",
        readonly=True,
        style=toga.style.Pack(flex=1),
    )

    token_password_input = toga.PasswordInput(
        placeholder="Token password", style=toga.style.Pack(flex=1)
    )

    output_file_input = toga.TextInput(
        placeholder="Output audio file path",
        readonly=True,
        style=toga.style.Pack(flex=1),
    )

    async def on_select_pdf(widget):
        try:
            file_path = await navigator.main_window.open_file_dialog(
                title="Select PDF File", file_types=["pdf"]
            )
            if file_path:
                pdf_file_input.value = str(file_path)
        except Exception as e:
            dialog = toga.ErrorDialog(
                title="Error", message=f"File selection error: {e}"
            )
            await navigator.main_window.dialog(dialog)

    async def on_select_token(widget):
        try:
            file_path = await navigator.main_window.open_file_dialog(
                title="Select Credentials Token File"
            )
            if file_path:
                token_path_input.value = str(file_path)
        except Exception as e:
            dialog = toga.ErrorDialog(
                title="Error", message=f"File selection error: {e}"
            )
            await navigator.main_window.dialog(dialog)

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
            dialog = toga.ErrorDialog(
                title="Error", message=f"File selection error: {e}"
            )
            await navigator.main_window.dialog(dialog)

    async def on_convert(widget):
        if not all(
            [
                pdf_file_input.value,
                token_path_input.value,
                token_password_input.value,
                output_file_input.value,
            ]
        ):
            dialog = toga.ErrorDialog(
                title="Error", message="Please fill in all required fields"
            )
            await navigator.main_window.dialog(dialog)
            return

        try:
            result = convert_pdf_to_audio(
                navigator.session,
                pdf_file_input.value,
                token_path_input.value,
                token_password_input.value,
                navigator.app_paths,
            )

            if result.is_ok():
                audio_bytes = result.unwrap()

                # Save audio to file
                with open(output_file_input.value, "wb") as f:
                    f.write(audio_bytes)

                success_dialog = toga.InfoDialog(
                    title="Success",
                    message=f"Audio file saved successfully!\n{output_file_input.value}",
                )
                await navigator.main_window.dialog(success_dialog)
            else:
                error_dialog = toga.ErrorDialog(
                    title="Error",
                    message=f"Failed to convert PDF: {result.unwrap_err()}",
                )
                await navigator.main_window.dialog(error_dialog)
        except Exception as e:
            dialog = toga.ErrorDialog(title="Error", message=f"Conversion error: {e}")
            await navigator.main_window.dialog(dialog)

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
                style=toga.style.Pack(direction=toga.style.pack.ROW, gap=5),
            ),
            toga.Label("Credentials Token:"),
            toga.Box(
                children=[
                    token_path_input,
                    toga.Button("Browse", on_press=on_select_token),
                ],
                style=toga.style.Pack(direction=toga.style.pack.ROW, gap=5),
            ),
            toga.Label("Token Password:"),
            token_password_input,
            toga.Label("Output Audio File:"),
            toga.Box(
                children=[
                    output_file_input,
                    toga.Button("Browse", on_press=on_select_output),
                ],
                style=toga.style.Pack(direction=toga.style.pack.ROW, gap=5),
            ),
            toga.Box(
                children=[
                    toga.Button("Convert", on_press=on_convert),
                    toga.Button("Cancel", on_press=on_cancel),
                ],
                style=toga.style.Pack(
                    direction=toga.style.pack.ROW, margin=(20, 0, 0, 0), gap=10
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
