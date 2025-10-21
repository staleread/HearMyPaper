from datetime import datetime


class Submission:
    def __init__(
        self,
        id: int,
        project_student_id: int,
        title: str,
        content: bytes,
        submitted_at: datetime,
    ):
        self.id = id
        self.project_student_id = project_student_id
        self.title = title
        self.content = content
        self.submitted_at = submitted_at
