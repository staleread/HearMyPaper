from result import Ok
from ...shared.ui.catalog_screen import catalog_screen
from ..api import get_submissions


def submissions_catalog_screen(navigator):
    """
    Екран таблиці submissions (список робіт).
    """
    result = get_submissions(navigator.session)

    if result.is_ok():
        subs = result.unwrap()
        data = [
            [
                s.id,
                s.title,
                s.student_name,
                s.instructor_name,
                s.submitted_at.strftime("%Y-%m-%d %H:%M"),
            ]
            for s in subs
        ]
    else:
        data = []

    return catalog_screen(
        title="Submissions",
        headings=["ID", "Title", "Student", "Instructor", "Submitted At"],
        data=Ok(data),
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=[
            ("New Submission", lambda w: navigator.navigate("submission_upload_form")),
        ],
        on_activate=lambda row: navigator.navigate(
            "submission_info", submission_id=row[0]
        ),
    )
