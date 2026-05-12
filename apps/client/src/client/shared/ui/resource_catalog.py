from result import Ok
from ...shared.ui.catalog_screen import catalog_screen


def resource_catalog_screen(navigator):
    resources = [
        {"resource": "Search User"},
        {"resource": "Projects"},
        {"resource": "Conversions"},
    ]

    def on_row_activate(row):
        match getattr(row, "resource"):
            case "Search User":
                navigator.navigate("user_search")
            case "Projects":
                navigator.navigate("projects_catalog")
            case "Conversions":
                navigator.navigate("conversions_catalog")

    return catalog_screen(
        title="Resources",
        headings=["Resource"],
        data=Ok(resources),
        on_back=None,
        actions=None,
        on_activate=on_row_activate,
        empty_message=None,
    )
