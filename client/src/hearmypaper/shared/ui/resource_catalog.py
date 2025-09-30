from ...shared.ui.catalog_screen import catalog_screen


def resource_catalog_screen(navigator):
    """Main resource catalog screen"""
    resources = [
        {"id": "users", "name": "Users", "description": "Manage users"},
        {"id": "projects", "name": "Projects", "description": "Manage projects"},
    ]

    def on_resource_click(resource, nav):
        if resource["id"] == "users":
            nav.navigate("users_catalog")
        elif resource["id"] == "projects":
            nav.navigate("projects_catalog")

    return catalog_screen(
        title="HearMyPaper - Resources",
        items=resources,
        navigator=navigator,
        on_item_click=on_resource_click,
        actions=None,  # No actions on main catalog
    )
