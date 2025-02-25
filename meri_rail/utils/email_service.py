"""Mail Services"""

from utils.utils import get_model
from utils.constants import AppLabelsModel
from meri_rail.constants import EmailType
from django_extensions.db.models import ActivatorModel
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

Otp = get_model(**AppLabelsModel.OTP)
EmailTemplate = get_model(**AppLabelsModel.EMAIL_TEMPLATE)


class EmailService:
    """Email Service Class to Handle Mail"""

    @staticmethod
    def get_template(email_type: str):
        """Returns Email Template"""
        try:
            return EmailTemplate.objects.get(
                status=ActivatorModel.ACTIVE_STATUS, email_type=email_type
            )
        except EmailTemplate.DoesNotExist:
            return None

    @staticmethod
    def send_mail(
        subject: str,
        body: str,
        is_html: bool,
        to_email: list,
        template: str | None = None,
    ):
        """This function will be used to send email using celery task based on email template"""
        sender = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            subject=subject, from_email=sender, to=to_email, body=body
        )
        if is_html:
            msg.attach_alternative(template, "text/html")
        msg.send(fail_silently=False)
        return f"Email Send Successfully : Subject: {subject}"

    def registration_success_mail(self, user):
        """Send Registration Success Mail"""
        template = self.get_template(EmailType.REGISTRATION_SUCCESS)
        data = {"user": user.get_full_name()}
        if template:
            self.send_mail(
                subject=template.subject,
                body=template.body % data,
                is_html=template.is_html,
                to_email=[user.email],
                template=template.template.format(**data),
            )
        return "Email Template Not Found"
