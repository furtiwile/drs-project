
class MailFormatter:
    FOOTER = "\n\n---\nThis is a student project. If you received this email by mistake, please disregard it."

    @classmethod
    def role_promotion_format(cls, name: str):
        return {
            "subject": "Congratulations on Your Role Upgrade!",
            "content": f"Hello {name}!\n\nYour Role has been upgraded to Manager!\n\n{cls.FOOTER}"
        }
