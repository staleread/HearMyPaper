from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    instructor_full_name: str
    instructor_email: str
    deadline: str
    student_count: int


class ProjectListResponse(BaseModel):
    id: int
    title: str
    instructor_full_name: str
    deadline: str


class ProjectCreateRequest(BaseModel):
    title: str
    syllabus_summary: str
    description: str
    instructor_email: str
    deadline: str


class ProjectUpdateRequest(BaseModel):
    title: str
    syllabus_summary: str
    description: str
    instructor_email: str
    deadline: str


class ProjectCreateResponse(BaseModel):
    id: int


class StudentAssignmentRequest(BaseModel):
    student_emails: list[str]


class ProjectStudentResponse(BaseModel):
    id: int
    username: str
