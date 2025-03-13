from django_extensions.db.models import ActivatorModel, TimeStampedModel
from django.db.models import CharField, TextField, BooleanField, ForeignKey, CASCADE
from django.db import models
from meri_rail.constants import ModelVerbose, EmailType, RequestTypes


class EmailTemplate(ActivatorModel):
    name = CharField(max_length=255)
    subject = CharField(max_length=255)
    email_type = CharField(max_length=1024, choices=EmailType.get_choices())
    body = TextField()
    is_html = BooleanField(default=False)
    template = TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ModelVerbose.EMAIL_TEMPLATE
        verbose_name_plural = ModelVerbose.EMAIL_TEMPLATES


class Notification(TimeStampedModel):
    email_template = ForeignKey(EmailTemplate, on_delete=CASCADE)
    user = ForeignKey("users.User", on_delete=CASCADE)
    is_sent = BooleanField(default=False)

    def __str__(self):
        return f"{self.email_template.email_type} to {self.user.email}"

    class Meta:
        verbose_name = ModelVerbose.NOTIFICATION
        verbose_name_plural = ModelVerbose.NOTIFICATIONS


class Requests(TimeStampedModel, ActivatorModel):
    url = models.URLField(max_length=2048)
    method = models.CharField(
        max_length=10, choices=RequestTypes.get_choices(), default=RequestTypes.GET
    )
    headers = models.JSONField(default=dict)
    params = models.JSONField(default=dict)
    data = models.JSONField(default=dict)
