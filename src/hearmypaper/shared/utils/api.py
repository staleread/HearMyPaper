import cbor2
import requests
from result import Result, Ok, Err


def check_response(
    r: requests.Response, raw_data: bool = False, cbor_data: bool = False
) -> Result[dict | bytes, str]:
    """
    Check HTTP response and return Result.

    Args:
        r: HTTP response
        raw_data: If True, return raw bytes instead of parsing
        cbor_data: If True, parse response as CBOR instead of JSON

    Returns:
        Result with data (dict or bytes) or error message
    """
    if raw_data:
        if r.status_code in [200, 201]:
            return Ok(r.content)
        elif r.status_code == 401:
            return Err("Authentication required. Please log in again.")
        elif r.status_code == 403:
            return Err(
                "Access forbidden. You don't have permission for this operation."
            )
        elif r.status_code == 404:
            return Err("Resource not found.")
        elif r.status_code >= 500:
            return Err("Server error. Please try again later.")
        else:
            return Err(f"{r.status_code}: Request failed")

    if r.status_code in [200, 201]:
        try:
            if cbor_data:
                data = cbor2.loads(r.content)
            else:
                data = r.json()
            return Ok(data)
        except (ValueError, cbor2.CBORDecodeError):
            return Err(f"{r.status_code}: Invalid response format")

    # Error responses are always JSON
    try:
        error_data = r.json()
        error_message = error_data.get(
            "detail", error_data.get("error", "Something went wrong")
        )
    except (ValueError, Exception):
        error_message = "Invalid error response format"

    if r.status_code == 401:
        return Err("Authentication required. Please log in again.")
    elif r.status_code == 403:
        return Err("Access forbidden. You don't have permission for this operation.")
    elif r.status_code == 404:
        return Err("Resource not found.")
    elif r.status_code >= 500:
        return Err("Server error. Please try again later.")
    else:
        return Err(f"{r.status_code}: {error_message}")
