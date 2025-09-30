from pydantic import BaseModel, field_validator
from datetime import datetime
import re

from ..auth.enums import AccessLevel


# Auth DTOs
class ChallengeRequest(BaseModel):
    user_id: int


class ChallengeResponse(BaseModel):
    challenge: str


class LoginRequest(BaseModel):
    user_id: int
    challenge: str
    signature: str


class LoginResponse(BaseModel):
    token: str


# User DTOs
class UserCreateRequest(BaseModel):
    name: str
    surname: str
    email: str
    confidentiality_level: int
    integrity_levels: list[int]
    public_key: str
    expires_at: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("expires_at must be a valid ISO date string")
        return v


class UserUpdateRequest(BaseModel):
    name: str
    surname: str
    email: str
    confidentiality_level: int
    integrity_levels: list[int]
    expires_at: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        return v


class UserCreateResponse(BaseModel):
    id: int


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    confidentiality_level: int
    integrity_levels: list[int]
    expires_at: str


class UserListResponse(BaseModel):
    id: int
    full_name: str


class UserView(BaseModel):
    """DTO for user data as displayed in UI views"""

    id: int
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    expires_at: str

    @classmethod
    def from_response(cls, response: UserResponse) -> "UserView":
        """Convert server response to view DTO"""
        return cls(
            id=response.id,
            name=response.name,
            surname=response.surname,
            email=response.email,
            confidentiality_level=AccessLevel(response.confidentiality_level),
            integrity_levels=[
                AccessLevel(level) for level in response.integrity_levels
            ],
            expires_at=response.expires_at,
        )


class UserCreateDto(BaseModel):
    """DTO for user creation form data"""

    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    expires_at: str
    credentials_path: str
    credentials_password: str

    def to_request(self, public_key: str) -> UserCreateRequest:
        """Convert to API request format"""
        return UserCreateRequest(
            name=self.name,
            surname=self.surname,
            email=self.email,
            confidentiality_level=self.confidentiality_level.value,
            integrity_levels=[level.value for level in self.integrity_levels],
            public_key=public_key,
            expires_at=self.expires_at,
        )


class UserUpdateDto(BaseModel):
    """DTO for user update form data"""

    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    expires_at: str

    def to_request(self) -> UserUpdateRequest:
        """Convert to API request format"""
        return UserUpdateRequest(
            name=self.name,
            surname=self.surname,
            email=self.email,
            confidentiality_level=self.confidentiality_level.value,
            integrity_levels=[level.value for level in self.integrity_levels],
            expires_at=self.expires_at,
        )


# Project DTOs
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


class ProjectResponse(BaseModel):
    id: int
    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    instructor_username: str
    deadline: str
    student_count: int


class ProjectListResponse(BaseModel):
    id: int
    title: str
    instructor_username: str
    deadline: str


class ProjectView(BaseModel):
    """DTO for project data as displayed in UI views"""

    id: int
    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    instructor_username: str
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
    instructor_id: int
    deadline: str

    def to_request(self) -> ProjectCreateRequest:
        """Convert to API request format"""
        return ProjectCreateRequest(**self.model_dump())


class ProjectUpdateDto(BaseModel):
    """DTO for project update form data"""

    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    deadline: str

    def to_request(self) -> ProjectUpdateRequest:
        """Convert to API request format"""
        return ProjectUpdateRequest(**self.model_dump())
