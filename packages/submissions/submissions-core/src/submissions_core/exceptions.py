class SubmissionsError(Exception):
    pass


class SubmissionNotFoundError(SubmissionsError):
    pass


class SubmissionAlreadyExistsError(SubmissionsError):
    pass


class InvalidSubmissionStatusError(SubmissionsError):
    pass


class UnauthorizedSubmissionError(SubmissionsError):
    pass


class AccessDeniedError(SubmissionsError):
    pass


class ProjectNotFoundError(SubmissionsError):
    pass


class StudentNotFoundError(SubmissionsError):
    pass
