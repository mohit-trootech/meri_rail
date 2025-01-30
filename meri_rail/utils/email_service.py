"""Mail Services"""

from utils.utils import get_model
from logging import Logger

logger = Logger(__name__)
Otp = get_model(app_name="users", model_name="Otp")


class EmailService:
    """Email Service Class to Handle Mail"""

    # @staticmethod
    # def get_template(email_type: str):
    #     """Returns Email Template"""
    #     try:
    #         return EmailTemplate.objects.get(
    #             status=ActivatorModel.ACTIVE_STATUS, email_type=email_type
    #         )
    #     except EmailTemplate.DoesNotExist:
    #         return None

    # @staticmethod
    # def send_mail(
    #     subject: str,
    #     body: str,
    #     is_html: bool,
    #     to_email: list,
    #     template: str | None = None,
    # ):
    #     """This function will be used to send email using celery task based on email template"""
    #     sender = settings.EMAIL_HOST_USER
    #     msg = EmailMultiAlternatives(
    #         subject=subject, from_email=sender, to=to_email, body=body
    #     )
    #     if is_html:
    #         msg.attach_alternative(template, "text/html")
    #     msg.send(fail_silently=False)
    #     logger.info(f"Email Send Successfully : Subject: {subject}")
    #     return f"Email Send Successfully : Subject: {subject}"
