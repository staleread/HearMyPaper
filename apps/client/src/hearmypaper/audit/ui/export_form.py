import asyncio
import csv
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def audit_export_form_screen(navigator, logs_data, date):
    children = [
        toga.Label(
            "Export Audit Logs",
            style=Pack(font_size=18, font_weight="bold", margin=(0, 0, 10, 0)),
        ),
        toga.Label(
            "Export audit logs to a CSV file.",
            style=Pack(font_size=10, color="#666666", margin=(0, 0, 20, 0)),
        ),
    ]

    file_input = toga.TextInput(
        placeholder="Path to save CSV file",
        readonly=True,
        style=Pack(flex=1),
    )

    async def show_error(message: str):
        dialog = toga.ErrorDialog(title="Error", message=message)
        await navigator.main_window.dialog(dialog)

    async def show_info(message: str):
        dialog = toga.InfoDialog(title="Success", message=message)
        await navigator.main_window.dialog(dialog)

    async def on_select_file(widget):
        try:
            file_path = await navigator.main_window.save_file_dialog(
                title="Save Audit Logs CSV",
                suggested_filename=f"{date.strftime('%Y-%m-%d')}_audit.csv",
            )
            if file_path:
                file_input.value = str(file_path)
        except Exception as e:
            await show_error(f"File selection error: {e}")

    async def on_export(widget):
        if not file_input.value:
            await show_error("Please choose a file path!")
            return

        try:
            with open(file_input.value, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    ["Timestamp", "Action", "Success", "Reason", "User", "IP Address"]
                )
                for row in logs_data:
                    writer.writerow(row)

            await show_info("Audit logs exported successfully!")
            navigator.navigate("audit_catalog")
        except Exception as e:
            await show_error(f"Export failed: {e}")

    def on_cancel(widget):
        navigator.navigate("audit_catalog")

    children.extend(
        [
            toga.Label("Output File:"),
            toga.Box(
                children=[
                    file_input,
                    toga.Button("Browse", on_press=on_select_file),
                ],
                style=Pack(direction=ROW, gap=5),
            ),
            toga.Box(
                children=[
                    toga.Button(
                        "Export", on_press=lambda w: asyncio.create_task(on_export(w))
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
