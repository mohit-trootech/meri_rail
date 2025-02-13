from django.utils.timezone import now


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
            .strptime(item["availablityDate"], "%d-%m-%Y")
            .strftime("%Y-%m-%d"),
            "available": item["availablityStatus"],
        }
        for item in data["avlDayList"]
    ]
