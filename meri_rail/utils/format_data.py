from django.utils.timezone import now
from utils.constants import DD_MM_YYYY, AppLabelsModel
from utils.utils import get_model
from django.utils.timezone import datetime

Train = get_model(**AppLabelsModel.TRAIN)
Station = get_model(**AppLabelsModel.STATION)


def format_seat_availability(data: dict, **kwargs) -> dict:
    """
    Format Seat Availability Data
    :param data: dict
    :return: dict
    """
    return [
        {
            "quota": kwargs["quota"],
            "train_cls": kwargs["train_cls"],
            "dt": now()
            .strptime(item["availablityDate"], DD_MM_YYYY)
            .strftime("%Y-%m-%d"),
            "available": item["availablityStatus"],
        }
        for item in data["avlDayList"]
    ]


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
                "serial_number": (passenger["passengerSerialNumber"]),
                "quota": (passenger["passengerQuota"]),
                "nationality": (passenger["passengerNationality"]),
                "waitlist_type": (
                    passenger["waitListType"] if passenger.get("waitListType") else None
                ),
                "booking_status": (passenger["bookingStatus"]),
                "booking_coach": (
                    passenger["bookingCoachId"]
                    if passenger.get("bookingCoachId")
                    else None
                ),
                "booking_berth": (
                    passenger["bookingBerthNo"]
                    if passenger.get("bookingBerthNo")
                    else None
                ),
                "booking_details": (
                    passenger["bookingStatusDetails"]
                    if passenger.get("bookingStatusDetails")
                    else None
                ),
                "current_status": (passenger["currentStatus"]),
                "current_coach": (
                    passenger["currentCoachId"]
                    if passenger.get("currentCoachId")
                    else None
                ),
                "current_berth": (
                    passenger["currentBerthNo"]
                    if passenger.get("currentBerthNo")
                    else None
                ),
                "current_details": (
                    passenger["currentStatusDetails"]
                    if passenger.get("currentStatusDetails")
                    else None
                ),
            }
        )
    return passengers_list


def format_pnr_details_in_valid_format(data: dict) -> dict:
    """
    Format pnr details in valid format.
    :param data: dict
    :return: dict
    """
    train = Train.objects.get(number=data["trainNumber"]).id
    source = Station.objects.get(code=data["sourceStation"].upper()).id
    destination = Station.objects.get(code=data["destinationStation"].upper()).id
    boarding = Station.objects.get(code=data["reservationUpto"].upper()).id
    return {
        "pnr": data["pnrNumber"],
        "date_of_journey": parse_date_string(data["dateOfJourney"]),
        "train_id": train,
        "source_id": source,
        "destination_id": destination,
        "boarding_id": boarding,
        "journey_class": data["journeyClass"] if data.get("journeyClass") else None,
        "number_of_passengers": (
            data["numberOfpassenger"] if data.get("numberOfpassenger") else None
        ),
        "chart_status": data["chartStatus"] if data.get("chartStatus") else None,
        "cancel_status": (
            data["trainCancelStatus"] if data.get("trainCancelStatus") else None
        ),
        "booking_fare": data["bookingFare"] if data.get("bookingFare") else None,
        "ticket_fare": data["ticketFare"] if data.get("ticketFare") else None,
        "quota": data["quota"] if data.get("quota") else None,
        "vikalp_otp": data["vikalpStatus"] if data.get("vikalpStatus") else None,
        "booking_date": parse_date_string(data["bookingDate"]),
        "mobile_number": (
            "+91" + data["mobileNumber"] if data.get("mobileNumber") else None
        ),
        "distance": data["distance"] if data.get("distance") else None,
        "passengers": get_passenger_details_list(passengers=data["passengerList"]),
    }


def format_fare_serializer(data: dict, payload) -> dict:
    """
    Format fare serializer data
    :param data: dict
    :return: dict
    """
    train = Train.objects.get(number=payload["train"]).id
    from_station = Station.objects.get(code=payload["from_station"].upper()).id
    to_station = Station.objects.get(code=payload["to_station"].upper()).id
    return {
        "train_id": train,
        "from_station_id": from_station,
        "to_station_id": to_station,
        "distance": data["distance"],
        "total_fare": data["totalFare"],
        "quota": payload["quota"],
        "train_cls": payload["train_cls"],
        "breakdown": {
            "base_fare": data["baseFare"],
            "reservation_charge": (
                data.get("reservationCharge") if data.get("reservationCharge") else None
            ),
            "superfast_charge": (
                data.get("superfastCharge") if data.get("superfastCharge") else None
            ),
            "total_concession": (
                data.get("totalConcession") if data.get("totalConcession") else None
            ),
            "tatkal_fare": data.get("tatkalFare") if data.get("tatkalFare") else None,
            "gst_charge": data.get("gstCharge") if data.get("gstCharge") else None,
            "other_charge": (
                data.get("otherCharge") if data.get("otherCharge") else None
            ),
            "catering_charge": (
                data.get("cateringCharge") if data.get("cateringCharge") else None
            ),
            "dynamic_fare": (
                data.get("dynamicFare") if data.get("dynamicFare") else None
            ),
        },
    }
