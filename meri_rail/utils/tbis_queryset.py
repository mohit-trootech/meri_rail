from utils.utils import get_model

Train = get_model(app_label="trains", model_name="Train")
Route = get_model(app_label="trains", model_name="Route")


def find_trains_between_stations(
    station_from_code: str, station_to_code: str, date: str
):
    """
    Finds trains running between two stations.

    Args:
        station_from_code:str: The code of the starting station.
        station_to_code:str: The code of the destination station.
        date: str: The date of travel.


    Returns:
        A queryset of Train objects that run between the specified stations,
        or an empty queryset if no such trains are found.
    """

    trains_from = Route.objects.filter(station__code=station_from_code).values_list(
        "train", flat=True
    )
    trains_to = Route.objects.filter(station__code=station_to_code).values_list(
        "train", flat=True
    )
    common_trains = trains_from.intersection(trains_to)

    if not common_trains:
        return Train.objects.none()
    trains = Train.objects.filter(id__in=common_trains)

    valid_trains = []
    for train in trains:
        routes = Route.objects.filter(train=train).distinct()
        from_index = next(
            (
                i
                for i, route in enumerate(routes)
                if route.station.code == station_from_code
                and date.weekday() in route.runs_on_days
            ),
            None,
        )
        if from_index is None:
            continue
        to_index = next(
            (
                i
                for i, route in enumerate(routes)
                if route.station.code == station_to_code
            ),
            None,
        )

        if from_index is not None and to_index is not None and from_index < to_index:
            valid_trains.append(train.id)

    return Train.objects.filter(id__in=valid_trains)
