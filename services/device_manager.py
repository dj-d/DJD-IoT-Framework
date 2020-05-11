import requests
from services.logger_service import LoggerService

logging_service = LoggerService(name=__name__)

logger = logging_service.get_logger()


class DeviceManager:
    """
    Provide methods to manage DIY IoT devices
    """

    def __init__(self, ip=None, action_path=None):
        if ip is not None:
            if action_path is not None:
                self.action_path = ip + action_path
                self.status_path = ip + action_path + "/status"
                self.relay_number_path = ip + action_path + "/get_relay_number"

            self.get_type_path = ip + "/get_type"

        self.type = {"ps": "power_strip", "rc": "remote_controller", "lsc": "led_strip_controller"}
        self.path = {"ps": "/ps", "rc": "/rc", "lsc": "/rgb"}

    def send_action(self, params):
        """
        Send action that device will do

        :param params: JSON
        :return: JSON | HTML error code
        """

        try:
            res = requests.post(url=self.action_path, data=params)

            return {"status_code": res.status_code, "info": res.json()}
        except requests.exceptions.ConnectionError:
            logger.exception("device_manager -> send_action (500)")

            return 500
        except requests.exceptions.RequestException:
            logger.exception("device_manager -> send_action (400)")

            return 400

    def get_status(self):
        """
        Get status data of the device

        :return: JSON | HTML error code
        """

        try:
            res = requests.get(url=self.status_path)

            return {"status_code": res.status_code, "info": res.json()}
        except requests.exceptions.ConnectionError:
            logger.exception("device_manager -> get_status (500)")

            return 500
        except requests.exceptions.RequestException:
            logger.exception("device_manager -> get_status (400)")

            return 400

    def get_relay_number(self):
        """
        Get number of realy

        :return: JSON | HTML error code
        """

        try:
            return requests.get(url=self.relay_number_path).json()["number"]
        except requests.exceptions.ConnectionError:
            logger.exception("device_manager -> get_relay_number (500)")

            return 500
        except requests.exceptions.RequestException:
            logger.exception("device_manager -> get_relay_number (400)")

            return 400

    def get_device_type(self):
        """
        Get type of device

        :return: JSON | HTML error code
        """

        try:
            return requests.get(url=self.get_type_path).json()["type"]
        except requests.exceptions.ConnectionError:
            logger.exception("device_manager -> get_type (500)")

            return 500
        except requests.exceptions.RequestException:
            logger.exception("device_manager -> get_type (400)")

            return 400

    def get_types(self):
        """
        Get dict with all device type

        :return: dict()
        """

        return self.type

    def get_path(self, type):
        """
        Get path for API

        :param type: Device type
        :return: Path | False
        """

        if type == self.type["ps"]:
            return self.path["ps"]
        elif type == self.type["rc"]:
            return self.path["rc"]
        elif type == self.type["lsc"]:
            return self.path["lsc"]
        else:
            return False
