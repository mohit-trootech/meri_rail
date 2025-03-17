from websocket import create_connection
from json import dumps, loads
from logging import getLogger
from utils.constants import ErrorMessages, SocketUrl

logger = getLogger(__name__)


class SocketService:
    """Socket Service Class"""

    @classmethod
    def pnr_service(cls, data: dict) -> dict:
        pnr_data = {"type": "pnr_status", "data": data}
        try:
            ws = create_connection(SocketUrl.PNR_STATUS)
            ws.send(dumps(pnr_data))
            result = loads(ws.recv())
            return result
        except Exception as err:
            logger.error(ErrorMessages.ERROR_IN_SERVICE % "PNR" + str(err))
            return {}

    @classmethod
    def fare_service(cls, data: dict) -> dict:
        fare_data = {"type": "fare_enquiry", "data": data}
        try:
            ws = create_connection(SocketUrl.FARE_ENQUIRY)
            ws.send(dumps(fare_data))
            result = loads(ws.recv())
            return result
        except Exception as err:
            logger.error(ErrorMessages.ERROR_IN_SERVICE % "FARE" + str(err))
            return {}

    @classmethod
    def seat_availability_service(cls, data: dict) -> dict:
        seat_data = {"type": "seat_availability", "data": data}
        try:
            ws = create_connection(SocketUrl.SEAT_AVAILABILITY)
            ws.send(dumps(seat_data))
            result = loads(ws.recv())
            return result
        except Exception as err:
            logger.error(ErrorMessages.ERROR_IN_SERVICE % "SEAT" + str(err))
            return {}

    @classmethod
    def spot_train_service(cls, data: dict) -> dict:
        spot_data = {"type": "spot_train", "data": data}
        try:
            ws = create_connection(SocketUrl.SPOT_TRAIN)
            ws.send(dumps(spot_data))
            result = loads(ws.recv())
            return result
        except Exception as err:
            logger.error(ErrorMessages.ERROR_IN_SERVICE % "SPOT" + str(err))
            return {}

    @classmethod
    def train_schedule_service(cls, data: dict) -> dict:
        schedule_data = {"type": "train_schedule", "data": data}
        try:
            ws = create_connection(SocketUrl.TRAIN_SCHEDULE)
            ws.send(dumps(schedule_data))
            result = loads(ws.recv())
            return result
        except Exception as err:
            logger.error(ErrorMessages.ERROR_IN_SERVICE % "SCHEDULE" + str(err))
            return {}
