import logging
import os
import base64
from brevo_python import ApiClient, Configuration, TransactionalEmailsApi, SendSmtpEmail # type: ignore
from concurrent.futures import ThreadPoolExecutor

from app.domain.services.mail.imail_service import IMailService
from app.domain.types.mail_data import MailData

logger = logging.getLogger(__name__)

class MailService(IMailService):
    def __init__(self, max_workers: int = 10) -> None:
        api_key = os.getenv("BREVO_API_KEY")
        configuration = Configuration()
        configuration.api_key['api-key'] = api_key # type: ignore
        
        self.api_instance = TransactionalEmailsApi(
            ApiClient(configuration)
        )
        self.default_sender = {
            "email": os.getenv("BREVO_SENDER_MAIL"),
            "name": os.getenv("BREVO_SENDER_NAME")
        }

        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def send(self, to_email: str, subject: str, content: str, attachment_bytes: bytes | None = None, attachment_name: str | None = None) -> None:
        try:
            attachments = None

            if attachment_bytes is not None:
                encoded_file: str = base64.b64encode(attachment_bytes).decode("utf-8")

                attachments = [
                    {
                        "content": encoded_file,
                        "name": attachment_name or "download.pdf",
                    }
                ]

            send_smtp_email = SendSmtpEmail(
                sender=self.default_sender,
                to=[{"email": to_email}],
                subject=subject,
                text_content=content,
                attachment=attachments
            )            
            self.api_instance.send_transac_email(send_smtp_email) # type: ignore

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
        
    def send_async(self, to_email: str, mail_data: MailData, attachment_bytes: bytes | None = None, attachment_name: str | None = None) -> None:
        self._executor.submit(self.send, to_email, mail_data['subject'], mail_data['content'], attachment_bytes, attachment_name)

    def send_async_many(self, to_emails: list[str], mail_data: list[MailData], attachment_bytes: bytes | None = None, attachment_name: str | None = None) -> None:
        if len(to_emails) != len(mail_data):
            logger.error("to_emails and mails must have the same length")
            return
        
        for email, mail in zip(to_emails, mail_data):
            self.send_async(email, mail, attachment_bytes, attachment_name)