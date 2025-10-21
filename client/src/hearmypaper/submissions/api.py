import requests
from result import Ok, Err
from .dto import SubmissionResponse, SubmissionCreateRequest

BASE_URL = "https://localhost"  # заміни на реальний бекенд


def get_submissions(session: requests.Session):
    """
    Завантажує список submissions.
    Повертає Result[List[SubmissionResponse], str].
    """
    try:
        response = session.get(f"{BASE_URL}/submission")
        if response.status_code == 200:
            data = [SubmissionResponse(**item) for item in response.json()]
            return Ok(data)
        else:
            return Err(f"{response.status_code}: {response.text}")
    except Exception as e:
        return Err(str(e))


def create_submission(session: requests.Session, data: SubmissionCreateRequest):
    """
    Створює submission.
    """
    try:
        response = session.post(f"{BASE_URL}/submission", json=data.model_dump())
        if response.status_code == 200:
            return Ok(response.json()["id"])
        return Err(f"{response.status_code}: {response.text}")
    except Exception as e:
        return Err(str(e))


def get_instructor_key(session: requests.Session, project_id: int):
    """
    Отримує публічний ключ інструктора для шифрування файлу.
    """
    try:
        response = session.get(
            f"{BASE_URL}/submission/instructor_key", params={"project_id": project_id}
        )
        if response.status_code == 200:
            return Ok(response.json()["public_key"])
        return Err(f"{response.status_code}: {response.text}")
    except Exception as e:
        return Err(str(e))


def create_project_student_api(session: requests.Session):
    """
    Створює новий project_student на сервері.
    Повертає Result[dict, str] з ключем 'project_student_id'
    """
    try:
        response = session.post(f"{BASE_URL}/submission/create_project_student")
        if response.status_code == 200:
            return Ok(response.json())  # {"project_student_id": ...}
        return Err(f"{response.status_code}: {response.text}")
    except Exception as e:
        return Err(str(e))
