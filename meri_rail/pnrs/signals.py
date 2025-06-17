# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from utils.utils import get_model
# from utils.constants import AppLabelsModel
# from utils.calender_service import CalenderApiService
# from users.constants import ModelFields
# from pnrs.constants import EventBody
# from pnrs.api.serializers import PnrDetailSerializer

# Pnr = get_model(**AppLabelsModel.PNR)


# @receiver(post_save, sender=Pnr)
# def add_user_to_pnr(sender, instance, created, **kwargs):
#     """
#     Create Calender Event for PNR, Using Google Calendar API.
#     """
#     calender_service = CalenderApiService()
#     users = instance.users.all().difference(instance.emailed_users.all())
#     for user in users:
#         if user.activity_status == ModelFields.ACTIVE_STATUS:
#             if not calender_service.get_credentials(user):
#                 user.activity_status = ModelFields.INACTIVE_STATUS
#                 user.save(update_fields=["activity_status"])
#                 continue
#             serializer = PnrDetailSerializer(instance)
#             date_iso = instance.date_of_journey.isoformat()
#             time_iso = instance.train.route.get(
#                 station=instance.boarding
#             ).departure.isoformat()
#             ()
#             event = calender_service.create_event_body(
#                 title=EventBody.TITLE.format(**serializer.data),
#                 location=EventBody.LOCATION.format(**serializer.data),
#                 description=EventBody.DESCRIPTION.format(**serializer.data),
#                 date_time=EventBody.DATE_TIME % (date_iso, time_iso),
#             )
#             calender_service.create_calender_event(event)
#             instance.emailed_users.add(user)
#             instance.save()
#     return
