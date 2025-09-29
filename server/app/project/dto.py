from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    title: str
    syllabus_summary: str
    description: str
    instructor_username: str
    student_count: int
    deadline: str


class ProjectListResponse(BaseModel):
    id: int
    title: str
    instructor_username: str
    deadline: str


class ProjectCreateRequest(BaseModel):
    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    deadline: str


class ProjectUpdateRequest(BaseModel):
    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    deadline: str


class ProjectCreateResponse(BaseModel):
    id: int


class StudentAssignmentRequest(BaseModel):
    student_ids: list[int]


class ProjectStudentResponse(BaseModel):
    id: int
    username: str
