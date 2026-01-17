import logging
import os
from threading import Thread
from brevo_python import ApiClient, Configuration, TransactionalEmailsApi, SendSmtpEmail

from app.domain.services.mail.imail_service import IMailService

logger = logging.getLogger(__name__)

class MailService(IMailService):
    def __init__(self):
        api_key = os.getenv("BREVO_API_KEY")
        configuration = Configuration()
        configuration.api_key['api-key'] = api_key
        
        self.api_instance = TransactionalEmailsApi(
            ApiClient(configuration)
        )
        self.default_sender = {
            "email": os.getenv("BREVO_SENDER_MAIL"),
            "name": os.getenv("BREVO_SENDER_NAME")
        }

    def send(self, to_email: str, subject: str, content: str):
        try:
            send_smtp_email = SendSmtpEmail(
                sender=self.default_sender,
                to=[{"email": to_email}],
                subject=subject,
                text_content=content
            )            
            self.api_instance.send_transac_email(send_smtp_email)

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
        
    def send_async(self, to_email: str, mail_data: dict[str, str]):
        thread = Thread(target=self.send, args=(to_email, mail_data.get('subject'), mail_data.get('content')))
        thread.daemon = True
        thread.start()