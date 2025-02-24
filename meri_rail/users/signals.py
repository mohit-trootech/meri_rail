"""Signals to handle User model related tasks"""

from utils.utils import get_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from users.constants import AUTHENTICATED_USER_CACHE_KEY

User = get_model("users", "User")


@receiver(post_save, sender=User)
def remove_cache(sender, instance, created, **kwargs):
    """Remove Cache When User Created"""
    cached_data = cache.get(AUTHENTICATED_USER_CACHE_KEY % instance.email)
    if cached_data:
        cache.delete(AUTHENTICATED_USER_CACHE_KEY % instance.email)
    return True


@receiver(post_save, sender=User)
def send_registration_mail(sender, instance, created, **kwargs):
    """Send Registration Mail When User Created"""
    if created:
        return True
    return False
