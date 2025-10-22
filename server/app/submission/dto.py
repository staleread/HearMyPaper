from pydantic import BaseModel


class SubmissionResponse(BaseModel):
    id: int
    title: str
    student_name: str
    instructor_name: str
    submitted_at: str
    content_hash: str


class SubmissionHashResponse(BaseModel):
    content_hash: str


class SubmissionContentResponse(BaseModel):
    encrypted_content: bytes
