"""Signals to handle User model related tasks"""

from utils.utils import get_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_model("users", "User")


@receiver(post_save, sender=User)
def send_registration_mail(sender, instance, created, **kwargs):
    """Send Registration Mail When User Created"""
    if created:
        return True
    return False
