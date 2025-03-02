from utils.utils import get_model
from utils.constants import AppLabelsModel
from celery import shared_task
from utils.email_service import EmailService

User = get_model(**AppLabelsModel.USERS)


@shared_task
def registration_email(id: int) -> None:
    """
    task to send registration email to user

    :param id: int
    """
    email_service = EmailService()
    return email_service.registration_success_mail(user=User.objects.get(id=id))
