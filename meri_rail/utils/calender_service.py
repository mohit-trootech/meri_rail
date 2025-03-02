from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.constants import CacheTimeout

# If modifying these scopes, delete the file token.json.\
# user meial and details


class CalenderApiService:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]
    creds = None

    def get_credentials(self, user) -> bool:
        credentials = settings.CREDENTIALS_CONFIG
        credentials.update(user.get_credentials)
        self.creds = Credentials.from_authorized_user_info(credentials, self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                return True
        return False

    def create_event_body(
        self,
        title: str,
        location: str,
        description: str,
        date_time: str,
        attendees: list = [],
    ) -> dict:
        return {
            "summary": title,
            "location": location,
            "description": description,
            "start": {
                "dateTime": date_time,
                "timeZone": settings.TIME_ZONE or "Asia/Kolkata",
            },
            "end": {
                "dateTime": date_time,
                "timeZone": settings.TIME_ZONE or "Asia/Kolkata",
            },
            "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
            "attendees": attendees,
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": CacheTimeout.x_minutes(60)},
                    {"method": "popup", "minutes": CacheTimeout.THIRTY_MINUTES},
                ],
            },
        }

    def create_calender_event(self, event: dict) -> None:
        service = build("calendar", "v3", credentials=self.creds)
        try:
            event = service.events().insert(calendarId="primary", body=event).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")


# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("fixtures/google/token.json"):
#         creds = Credentials.from_authorized_user_file(
#             settings.CREDENTIALS_JSON,
#             SCOPES,
#         )
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_config(
#                 settings.TOKEN_JSON,
#                 SCOPES,
#             )
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("calendar", "v3", credentials=creds)

#         # Call the Calendar API
#         now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
#         print("Getting the upcoming 10 events")
#         events_result = (
#             service.events()
#             .list(
#                 calendarId="primary",
#                 timeMin=now,
#                 maxResults=10,
#                 singleEvents=True,
#                 orderBy="startTime",
#             )
#             .execute()
#         )
#         events = events_result.get("items", [])
#         # event = {
#         #     "summary": "Google I/O 2015",
#         #     "location": "800 Howard St., San Francisco, CA 94103",
#         #     "description": "A chance to hear more about Google's developer products.",
#         #     "start": {
#         #         "dateTime": "2015-05-28T09:00:00-07:00",
#         #         "timeZone": "America/Los_Angeles",
#         #     },
#         #     "end": {
#         #         "dateTime": "2015-05-28T17:00:00-07:00",
#         #         "timeZone": "America/Los_Angeles",
#         #     },
#         #     "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
#         #     "attendees": [
#         #         {"email": "lpage@example.com"},
#         #         {"email": "sbrin@example.com"},
#         #     ],
#         #     "reminders": {
#         #         "useDefault": False,
#         #         "overrides": [
#         #             {"method": "email", "minutes": 24 * 60},
#         #             {"method": "popup", "minutes": 10},
#         #         ],
#         #     },
#         # }

#         # event = service.events().insert(calendarId='primary', body=event).execute()
#         # print 'Event created: %s' % (event.get('htmlLink'))

#         if not events:
#             print("No upcoming events found.")
#             return

#         # Prints the start and name of the next 10 events
#         for event in events:
#             start = event["start"].get("dateTime", event["start"].get("date"))
#             print(start, event["summary"])

#     except HttpError as error:
#         print(f"An error occurred: {error}")


# if __name__ == "__main__":
#     main()
