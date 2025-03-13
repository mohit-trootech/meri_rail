from websocket import create_connection
from json import dumps, loads
from logging import getLogger

logger = getLogger(__name__)


class SocketService:
    """Socket Service Class"""

    SOCKET_URL = "ws://localhost:8001/"

    @classmethod
    def pnr_service(cls, data: dict) -> dict:
        pnr_data = {"type": "pnr_status", "data": data}
        try:
            ws = create_connection(cls.SOCKET_URL + "ws/pnr/")
            ws.send(dumps(pnr_data))
            result = loads(ws.recv())
            if "error" in result:
                pass
            return result
        except Exception as err:
            logger.error(f"Error in pnr_service: {err}")
            return {}
