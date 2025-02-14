from django.contrib.admin import register, ModelAdmin
from utils.utils import get_model

EmailTemplate = get_model(app_label="meri_rail", model_name="EmailTemplate")
Notification = get_model(app_label="meri_rail", model_name="Notification")


@register(EmailTemplate)
class EmailTemplateAdmin(ModelAdmin):
    list_display = ("name", "subject", "email_type", "is_html")
    search_fields = ("name", "subject", "email_type")


@register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ("email_template", "user", "is_sent", "created")
    search_fields = ("email_template__name", "user__email")
    list_filter = ("is_sent", "created")
