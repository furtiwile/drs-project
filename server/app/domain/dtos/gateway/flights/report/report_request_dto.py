from dataclasses import dataclass
from typing import Any, Self

@dataclass
class ReportRequestDTO:
    report_types: list[str] | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            report_types=data.get('report_types')
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_types": self.report_types
        }

