from pydantic import BaseModel


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


class ProjectView(BaseModel):
    """DTO for project data as displayed in UI views"""

    id: int
    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    instructor_full_name: str
    instructor_email: str
    deadline: str
    student_count: int

    @classmethod
    def from_response(cls, response: ProjectResponse) -> "ProjectView":
        """Convert server response to view DTO"""
        return cls(**response.model_dump())


class ProjectCreateDto(BaseModel):
    """DTO for project creation form data"""

    title: str
    syllabus_summary: str
    description: str
    instructor_email: str
    deadline: str

    def to_request(self) -> ProjectCreateRequest:
        """Convert to API request format"""
        return ProjectCreateRequest(**self.model_dump())


class ProjectUpdateDto(BaseModel):
    """DTO for project update form data"""

    title: str
    syllabus_summary: str
    description: str
    instructor_email: str
    deadline: str

    def to_request(self) -> ProjectUpdateRequest:
        """Convert to API request format"""
        return ProjectUpdateRequest(**self.model_dump())
