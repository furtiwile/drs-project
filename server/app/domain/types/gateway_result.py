from dataclasses import dataclass
from typing import Generic, TypeVar, Union

T = TypeVar("T")

@dataclass(frozen=True)
class ok(Generic[T]):
    data: T
    success: bool = True

@dataclass(frozen=True)
class err:
    status_code: int
    message: str
    success: bool = False

GatewayResult = Union[ok[T], err]