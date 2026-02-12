from abc import ABC, abstractmethod

from app.domain.types.mail_data import MailData

class IMailService(ABC):
    @abstractmethod
    def send(self, to_email: str, subject: str, content: str) -> None:
        pass

    @abstractmethod
    def send_async(self, to_email: str, mail_data: MailData, attachment_bytes: bytes | None = None, attachment_name: str | None = None) -> None:
        pass

    @abstractmethod
    def send_async_many(self, to_emails: list[str], mail_data: list[MailData], attachment_bytes: bytes | None = None, attachment_name: str | None = None) -> None:
        pass