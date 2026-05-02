from result import Ok
from ...shared.ui.item_info_screen import item_info_screen
from .. import service


def submission_info_screen(navigator, submission_id):
    result = service.list_submissions(navigator.session)

    if result.is_err():
        data = result
    else:
        submissions = result.unwrap()
        submission = next((s for s in submissions if s.id == submission_id), None)

        if submission:
            data = Ok(submission.model_dump())
        else:
            data = result.map_err(lambda _: "Submission not found")

    def on_open():
        navigator.navigate("submission_open_form", submission_id=submission_id)

    def on_pdf_to_audio():
        navigator.navigate("submission_convert_form", submission_id=submission_id)

    actions = [
        ("Open", on_open),
        ("PDF to Audio", on_pdf_to_audio),
    ]

    return item_info_screen(
        title="Submission Details",
        data=data,
        on_back=lambda w: navigator.navigate("submissions_catalog"),
        actions=actions,
    )
