import toga
import asyncio
from result import Ok
from ...shared.ui.catalog_screen import catalog_screen
from client_core.models import ConversionStatus


def conversions_catalog_screen(navigator):
    async def load_conversions():
        try:
            conversions = await navigator.get_my_conversions_use_case()
            return [
                {
                    "id": str(c.id),
                    "source_id": str(c.source_id),
                    "status": c.status.value,
                    "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
                }
                for c in conversions
            ]
        except Exception as e:
            await navigator.main_window.dialog(
                toga.ErrorDialog("Error", f"Failed to load conversions: {e}")
            )
            return []

    async def on_row_activate(row):
        status = getattr(row, "status")
        conversion_id = getattr(row, "id")

        if status == ConversionStatus.COMPLETED.value:
            navigator.navigate("conversion_download_form", conversion_id=conversion_id)
        else:
            await navigator.main_window.dialog(
                toga.InfoDialog(
                    "Conversion Status",
                    f"This conversion is currently {status}. Please wait until it is completed.",
                )
            )

    return catalog_screen(
        title="My Conversions",
        headings=["ID", "Source ID", "Status", "Created At"],
        data=Ok([]),
        on_back=lambda w: navigator.navigate("resource_catalog"),
        on_activate=lambda row: asyncio.create_task(on_row_activate(row)),
        on_refresh=load_conversions,
    )
