class EducationError(Exception):
    pass


class ProjectAlreadyExistsError(EducationError):
    pass


class ProjectNotFoundError(EducationError):
    pass


class AttemptNotFoundError(EducationError):
    pass


class AccessDeniedError(EducationError):
    pass


class StudentNotFoundError(EducationError):
    pass


class StudentAlreadyAssignedError(EducationError):
    pass


class StudentNotAssignedError(EducationError):
    pass
