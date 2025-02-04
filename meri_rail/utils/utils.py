"""Utilities Functions for PNR Scrapping"""

from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.utils.timezone import datetime
from trains.models import Train
from stations.models import Station


def load_data(filepath: str) -> dict:
    """
    Load data from json file.
    :param filepath: str
    :return: dict
    """
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


def get_model(app_label, model_name):
    """Returns Model Instance"""
    from django.apps import apps

    return apps.get_model(app_label=app_label, model_name=model_name)


def parse_date_string(date: str):
    """
    Parse date string to datetime object.
    :param date: str
    :return: datetime object
    """
    return datetime.strptime(date, "%b %d, %Y %I:%M:%S %p").date()


def get_passenger_details_list(passengers: dict) -> list:
    """
    Generate passenger details list.
    :param passengers: dict
    :return: list
    """
    passengers_list = []
    for passenger in passengers:
        passengers_list.append(
            {
                "serial_number": passenger["passengerSerialNumber"],
                "quota": passenger["passengerQuota"],
                "nationality": passenger["passengerNationality"],
                "waitlist_type": passenger["waitListType"],
                "booking_status": passenger["bookingStatus"],
                "booking_coach": passenger["bookingCoachId"],
                "booking_berth": passenger["bookingBerthNo"],
                "booking_details": passenger["bookingStatusDetails"],
                "current_status": passenger["currentStatus"],
                "current_coach": passenger["currentCoachId"],
                "current_berth": passenger["currentBerthNo"],
                "current_details": passenger["currentStatusDetails"],
            }
        )
    return passengers_list


def format_pnr_details_in_valid_format(data: dict) -> dict:
    """
    Format pnr details in valid format.
    :param data: dict
    :return: dict
    """
    train = Train.objects.get(number=data["trainNumber"])
    source = Station.objects.get(code=data["sourceStation"])
    destination = Station.objects.get(code=data["destinationStation"])
    boarding = Station.objects.get(code=data["reservationUpto"])
    return {
        "pnr": data["pnrNumber"],
        "date_of_journey": parse_date_string(data["dateOfJourney"]),
        "train": train,
        "source": source,
        "destination": destination,
        "boarding": boarding,
        "journey_class": data["journeyClass"],
        "number_of_passengers": data["numberOfpassenger"],
        "chart_status": data["chartStatus"],
        "cancel_status": data["trainCancelStatus"],
        "booking_fare": data["bookingFare"],
        "ticket_fare": data["ticketFare"],
        "quota": data["quota"],
        "vikalp_otp": data["vikalpStatus"],
        "booking_date": parse_date_string(data["bookingDate"]),
        "mobile_number": "+91" + data["mobileNumber"],
        "distance": data["distance"],
        "passengers": get_passenger_details_list(passengers=data["passengerList"]),
    }


class AuthService:
    def __tokens_for_user(self, user) -> dict:
        """generate tokens"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_auth_tokens_for_user(self, user) -> dict:
        """call private method to generate refresh and access token"""
        return self.__tokens_for_user(user)
