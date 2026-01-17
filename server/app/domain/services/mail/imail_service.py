from abc import abstractmethod

from app.domain.types.mail_data import MailData

class IMailService:
    @abstractmethod
    def send(self, to_email: str, subject: str, content: str) -> None:
        pass

    @abstractmethod
    def send_async(self, to_email: str, mail_data: MailData) -> None:
        pass