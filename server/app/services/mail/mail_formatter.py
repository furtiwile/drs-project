from app.domain.types.mail_data import MailData
from app.domain.dtos.gateway.flights.flight.flight_dto import FlightDTO
from app.domain.models.user import User

class MailFormatter:
    FOOTER = "\n\n---\nThis is a student project. If you received this email by mistake, please disregard it."

    @classmethod
    def role_promotion_format(cls, user: User) -> MailData:
        return {
            "subject": "Congratulations on Your Role Upgrade!",
            "content": f"Hello {user.first_name}!\n\nYour Role has been upgraded to Manager!\n\n{cls.FOOTER}"
        }

    @classmethod
    def flight_cancelled_format(cls, users: list[User], flight: FlightDTO | None) -> list[MailData]:
        if flight is None:
            return []
        
        mails: list[MailData] = []
        for user in users:
            mails.append(
                MailData(
                    subject="Flight cancellation",
                    content=f"Hello {user.first_name}!\n\nYour flight '{flight.flight_name}' has been cancelled!\n\n{cls.FOOTER}"
                )
            )
        
        return mails