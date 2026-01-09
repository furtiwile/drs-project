from dataclasses import dataclass
from typing import Generic, TypeVar, Union
from app.domain.enums.ErrorType import ErrorType

T = TypeVar("T")

@dataclass(frozen=True)
class ok(Generic[T]):
    data: T
    success: bool = True

@dataclass(frozen=True)
class err:
    status_code: ErrorType
    message: str
    success: bool = False

Result = Union[ok[T], err]