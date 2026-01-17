from abc import abstractmethod

class IMailService:
    @abstractmethod
    def send(self, to_email: str, subject: str, content: str):
        pass

    @abstractmethod
    def send_async(self, to_email: str, subject: str, content: str):
        pass