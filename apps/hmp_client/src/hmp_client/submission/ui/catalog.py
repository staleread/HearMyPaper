from ...shared.ui.catalog_screen import catalog_screen
from .. import service


def submissions_catalog_screen(navigator):
    data = (
        service.list_submissions(navigator.session)
        .map(
            lambda submissions: [submission.model_dump() for submission in submissions]
        )
        .map_err(lambda err: f"Error loading submissions: {err}")
    )

    return catalog_screen(
        title="Submissions",
        headings=["ID", "Title", "Student Name", "Instructor Name", "Submitted At"],
        data=data,
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=[],
        on_activate=lambda row: navigator.navigate(
            "submission_info", submission_id=row.id
        ),
    )
