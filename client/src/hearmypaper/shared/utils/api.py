import requests
from result import Result, Ok, Err


def check_response(r: requests.Response) -> Result[dict, str]:
    try:
        data = r.json()
    except ValueError:
        return Err(f"{r.status_code}: Invalid response format")

    if r.status_code in [200, 201]:
        return Ok(data)
    elif r.status_code == 401:
        return Err("Authentication required. Please log in again.")
    elif r.status_code == 403:
        return Err("Access forbidden. You don't have permission for this operation.")
    elif r.status_code == 404:
        return Err("Resource not found.")
    elif r.status_code >= 500:
        return Err("Server error. Please try again later.")
    else:
        error_message = data.get("detail", "Something went wrong")
        return Err(f"{r.status_code}: {error_message}")
