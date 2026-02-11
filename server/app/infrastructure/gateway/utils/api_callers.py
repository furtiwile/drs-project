import requests
from ast import TypeVar
from typing import Callable

from app.domain.types.result import Result, ok, err

T = TypeVar("T")

def make_api_call[T](
    operation: Callable[[], requests.Response],
    on_success: Callable[[requests.Response], T],
    success_codes: tuple[int, ...] = (200,)
) -> Result[T, int]:
    try:
        response = operation()
        
        if response.status_code in success_codes:
            return ok(on_success(response))
        
        error_msg = _extract_error_message(response)
        return err(response.status_code, error_msg)
    
    except Exception:
        return err(500, "Internal Gateway Error")


def _extract_error_message(response: requests.Response) -> str:
    content_type = response.headers.get("Content-Type", "")
    
    if content_type.startswith("application/json"):
        try:
            json_data = response.json()
            return json_data.get("error", json_data.get("message", response.text))
        except Exception:
            return response.text or "Unknown error"
    
    return response.text or "Unknown error"