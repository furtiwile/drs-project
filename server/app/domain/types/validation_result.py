from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationResult:
    success: bool
    message: str | None = None

    def __bool__(self):
        return self.success

    @staticmethod
    def ok() -> ValidationResult:
        return ValidationResult(True)

    @staticmethod
    def fail(message: str) -> ValidationResult:
        return ValidationResult(False, message)
