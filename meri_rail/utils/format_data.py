from utils.utils import get_model
from utils.utils import log_errors

Station = get_model(app_label="stations", model_name="Station")
Train = get_model(app_label="trains", model_name="Train")


def format_tbis_data(data: dict) -> dict:
    """
    Format TBIS data.
    :param data: dict
    :return: dict
    """
    from_station = Station.objects.get(code=data["fromStnCode"].upper())
    to_station = Station.objects.get(code=data["toStnCode"].upper())
    return {
        "from_station_id": from_station,
        "to_station_id": to_station,
    }


def format_tbis_trains_list(data: dict) -> dict:
    """
    Format TBIS trains list.
    :param data: dict
    :return: list of dict
    """
    tbis_data = []

    def format_tbis_inner(data):
        try:
            train_obj = Train.objects.get(number=train["trainNumber"])
            train_data = {
                "train_id": train_obj.id,
                "arrival_time": train["arrivalTime"],
                "departure_time": train["departureTime"],
                "distance": train["distance"],
                "duration": train["duration"],
                "on_monday": True if train["runningMon"] == "Y" else False,
                "on_tuesday": True if train["runningTue"] == "Y" else False,
                "on_wednesday": True if train["runningWed"] == "Y" else False,
                "on_thursday": True if train["runningThu"] == "Y" else False,
                "on_friday": True if train["runningFri"] == "Y" else False,
                "on_saturday": True if train["runningSat"] == "Y" else False,
                "on_sunday": True if train["runningSun"] == "Y" else False,
                "train_type": train["trainType"][0],
            }
            train_data.update(format_tbis_data(train))
            return train_data
        except Exception as e:
            log_errors(__name__, str(e))
            return

    for train in data["trainBtwnStnsList"]:
        temp_data = format_tbis_inner(data=train)
        if temp_data is not None:
            tbis_data.append(temp_data)
    for train in data["alternateTrainBtwnStnsList"]:
        temp_data = format_tbis_inner(data=train)
        if temp_data is not None:
            tbis_data.append(temp_data)
    return tbis_data
