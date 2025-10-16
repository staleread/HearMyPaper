from result import Ok
from ...shared.ui.catalog_screen import catalog_screen


def resource_catalog_screen(navigator, session):
    screen = catalog_screen(
        title="Resources",
        headings=["Name", "Type", "Owner"],
        data=Ok([]),
        # Захоплюємо session у лямбдах
        on_back=lambda w=None, s=session: navigator.navigate("home", session=s),
        on_activate=lambda row, s=session: navigator.navigate(
            "audit_catalog", session=s
        ),
        actions=None,
    )
    return screen
