from result import Ok
from ...shared.ui.catalog_screen import catalog_screen


def resource_catalog_screen(navigator):
    resources = [
        {"resource": "Users"},
        {"resource": "Projects"},
        {"resource": "Audit"},
        {"resource": "Submissions"},
    ]

    def on_row_activate(row):
        match row.resource:
            case "Users":
                navigator.navigate("users_catalog")
            case "Projects":
                navigator.navigate("projects_catalog")
            case "Audit":
                navigator.navigate("audit_catalog")
            case "Submissions":
                navigator.navigate("submissions_catalog")

    return catalog_screen(
        title="Resources",
        headings=["Resource"],
        data=Ok(resources),
        on_back=None,
        actions=None,
        on_activate=on_row_activate,
    )
