from models.device_model import DeviceModel, PowerStripModel
from devices_manager.diy_device_manager import DeviceManager

import hashlib
import json
import re

from services.logger_service import LoggerService

logging_service = LoggerService(name=__name__)

logger = logging_service.get_logger()


class DeviceService:
    """
    Provide methods to manage devices
    """

    def __init__(self):
        self.device_model = DeviceModel()
        self.power_strip_model = PowerStripModel()

        self.type = DeviceManager().get_types()

    @staticmethod
    def make_response(is_valid: bool, info, error_code: int):
        """
        Make response for client

        :param is_valid: The success of the operation
        :param info: Some information
        :param error_code: HTMl error code
        :return: dict()
        """

        return {'valid': is_valid, 'info': info, 'code': error_code}

    def manager(self, data: dict):
        """
        Manage the different actions

        :param data:
        :return: tuple()
        """

        if "device" not in data:
            if data["action"] == "create":
                return self.create(data["info"]["ip"])
            elif data["action"] == "delete":
                return self.delete(data["info"]["device_id"])
            elif data["action"] == "change_ps_name":
                return self.ps_change_name(data["info"]["device_id"], data["info"]["new_name"])
            elif data["action"] == "change_switch_name":
                return self.ps_change_switch_name(data["info"]["device_id"], data["info"]["switch_number"], data["info"]["new_name"])
            elif data["action"] == "send":
                return self.send_action(data["info"]["id"], data["info"]["params"])
            elif data["action"] == "get":
                return self.get_status(data["info"]["id"])
            else:
                return self.make_response(False, "Not valid action", 400)

    @staticmethod
    def check_ip(ip: str):
        """
        Check if is a valid ip

        :param ip:
        :return: ip | False
        """

        regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

        if "http://" not in ip:
            i = 0
            while i < len(ip) and not ip[i].isdigit():
                i += 1

            sub_ip = ip[i:]
        else:
            sub_ip = ip[7:]

        if re.search(regex, sub_ip):
            return "http://" + sub_ip

        return False

    def is_valid_type(self, type: str):
        """
        Check if is a valid type

        :param type:
        :return: True | False
        """
        if type == self.type["ps"] or type == self.type["rc"] or type == self.type["lsc"]:
            return True

        return False

    @staticmethod
    def id_creator(ip: str, type: str):
        """
        Create id of device by:

        :param ip:
        :param type:
        :return: sha_signature
        """
        hash_string = ip + type
        sha_signature = hashlib.sha1(hash_string.encode()).hexdigest()

        return sha_signature

    def create(self, ip: str):
        """
        Create new device

        :param ip: IP of the device
        :return: tuple()
        """

        checked_ip = self.check_ip(ip)

        if checked_ip:
            type = DeviceManager(checked_ip).get_device_type()

            if self.is_valid_type(type):
                id = self.id_creator(checked_ip, type)
                path = DeviceManager().get_path(type)

                if not self.device_model.check_id(id):
                    if not self.device_model.create(id, checked_ip, type, path):
                        logger.error("device_service -> device not added")

                        return self.make_response(False, "Error", 500)

                    if type == self.type["ps"]:
                        if not self.ps_create(id, DeviceManager(checked_ip, path).get_relay_number()):
                            logger.error("device_service -> power strip data for id \"" + id + "\" not added")

                    return self.make_response(True, id, 201)

        return self.make_response(False, "Not valid input", 400)

    def delete(self, id: str):
        """
        Delete device by:

        :param id:
        :return: tuple()
        """

        if self.device_model.check_id(id):
            if self.power_strip_model.delete(id) and self.device_model.delete(id):
                return self.make_response(True, "Ok", 200)
            else:
                logger.error("device_service -> delete_device")

                return self.make_response(False, "Error", 500)
        else:
            logger.error("device_service -> delete_device")

            return self.make_response(False, "Not valid id", 400)

    def ps_create(self, id: str, number: int):
        """
        Create power strip with their default data

        :param id: ID of the device
        :param number: Number of relay
        :return: True | False
        """

        try:
            i = 0
            while True:
                i += 1
                name = "PS_" + str(i)

                if not self.power_strip_model.check_name(name):
                    break

            for num in range(number):
                switch_name = "Switch " + str(num)
                self.power_strip_model.create(id, name, num, switch_name)

            return True
        except Exception:
            logger.exception("device_service -> create_power_strip")

            return False

    def ps_change_name(self, id: str, new_name: str):
        """
        Update name of a specific power strip

        :param id: ID of device
        :param new_name:
        :return: True | False
        """

        if self.device_model.check_id(id):
            if self.power_strip_model.update_name(id, new_name):
                return self.make_response(True, "Ok", 200)
            else:
                return self.make_response(False, "Error", 500)
        else:
            logger.error("device_service -> ps_change_name")

            return self.make_response(False, "Not valid id", 400)

    def ps_change_switch_name(self, id: str, switch_number: int, new_name: str):
        """
        Change name of a specific switch of specific power strip

        :param id: ID of device
        :param switch_number:
        :param new_name:
        :return: True | False
        """

        if self.device_model.check_id(id):
            if 0 <= (switch_number - 1) < self.power_strip_model.get_switch_number(id):
                if self.power_strip_model.update_switch_name(id, switch_number, new_name):
                    return self.make_response(True, "Ok", 200)
                else:
                    return self.make_response(False, "Error", 500)
            else:
                return self.make_response(False, "Not valid switch number", 400)
        else:
            logger.error("device_service -> ps_change_name")

            return self.make_response(False, "Not valid id", 400)

    def send_action(self, id, params):
        if self.device_model.check_id(id):
            ip = self.device_model.get_ip(id)
            path = self.device_model.get_path(id)

            res = DeviceManager(ip, path).send_action(json.dumps(params))

            if res["status_code"] == 200:
                return self.make_response(True, res["info"]["msg"], res["status_code"])
            elif res["status_code"] == 500:
                return self.make_response(False, res["info"]["msg"], res["status_code"])
            elif res["status_code"] == 400:
                return self.make_response(False, res["info"]["msg"], res["status_code"])
            elif res == 500:
                return self.make_response(False, "Server error", res)
            else:
                return self.make_response(False, "Request error", res)

    def get_status(self, id):
        if self.device_model.check_id(id):
            ip = self.device_model.get_ip(id)
            path = self.device_model.get_path(id)

            res = DeviceManager(ip, path).get_status()

            if res["status_code"] == 200:
                return self.make_response(True, res["info"], res["status_code"])
            elif res["status_code"] == 500:
                return self.make_response(False, res["info"]["msg"], res["status_code"])
            elif res["status_code"] == 400:
                return self.make_response(False, res["info"]["msg"], res["status_code"])
            elif res == 500:
                return self.make_response(False, "Server error", res)
            else:
                return self.make_response(False, "Request error", res)
