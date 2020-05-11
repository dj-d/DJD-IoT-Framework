import mysql.connector as mysql
from database.database import Database
from services.logger_service import LoggerService

logging_service = LoggerService(name=__name__)

logger = logging_service.get_logger()


class DeviceSchema:
    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

        self.create_device_table()
        self.create_power_strip_table()

    def __del__(self):
        self.conn.close()

    def create_device_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS device (
                    id CHAR(40) NOT NULL UNIQUE PRIMARY KEY,
                    ip CHAR(22) NOT NULL,
                    type VARCHAR(255) NOT NULL,
                    path VARCHAR(10)
                )
                """

        self.curs.execute(query)
        self.conn.commit()

    def create_power_strip_table(self):
        """
        Init power_strip table

        :return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS power_strip (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    device_id CHAR(40),
                    name VARCHAR(255) NOT NULL,
                    switch_number INT NOT NULL,
                    switch_name VARCHAR(255) NOT NULL,
                    FOREIGN KEY (device_id)
                        REFERENCES device(id)
                        ON DELETE CASCADE 
                );
                """

        self.curs.execute(query)
        self.conn.commit()


class DeviceModel:
    """
    Provide methods for device data management into the DB
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

    def create(self, id, ip, type, path):
        """
        Create new device

        :param id:
        :param ip:
        :param type:
        :return: True | False
        """

        query = """
                INSERT INTO device (id, ip, type, path)
                VALUES (%s, %s, %s, %s)
                """

        try:
            self.curs.execute(query, (id, ip, type, path))
            self.conn.commit()

            return True
        except mysql.Error:
            logger.exception("device_model -> create_device")

            return False

    def delete(self, id):
        """
        Delete device by:

        :param id:
        :return: True | False
        """

        query = """
                DELETE FROM device
                WHERE id=%s
                """

        try:
            self.curs.execute(query, (id,))
            self.conn.commit()

            return True
        except mysql.Error:
            logger.exception("device_model -> delete_device")

            return False

    def check_id(self, id):
        """
        Check if id exists into the DB

        :param id:
        :return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT *
                    FROM device
                    WHERE id=%s
                )
                """

        try:
            self.curs.execute(query, (id,))
            res = self.curs.fetchone()
            self.conn.commit()

            return bool(res[0])
        except mysql.Error:
            logger.exception("device_model -> check_id")

            return False

    def get_ip(self, id):
        query = """
                SELECT ip
                FROM device
                WHERE id=%s
                """

        try:
            self.curs.execute(query, (id,))
            res = self.curs.fetchone()
            self.conn.commit()

            return res[0]
        except mysql.Error:
            logger.exception("device_model -> get_ip")

            return False

    def get_path(self, id):
        query = """
                SELECT path
                FROM device
                WHERE id=%s
                """

        try:
            self.curs.execute(query, (id,))
            res = self.curs.fetchone()
            self.conn.commit()

            return res[0]
        except mysql.Error:
            logger.exception("device_model -> get_path")

            return False


class PowerStripModel:
    """
    Provide methods for power_strip data management into the DB
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

    def create(self, device_id, name, switch_number, switch_name):
        """
        Create new power strip

        :param device_id:
        :param name: The name of the power strip
        :param switch_number:
        :param switch_name:
        :return: True | False
        """

        query = """
                INSERT INTO power_strip(device_id, name, switch_number, switch_name)
                VALUES (%s, %s, %s, %s)
                """

        try:
            self.curs.execute(query, (device_id, name, switch_number, switch_name))
            self.conn.commit()

            return True
        except mysql.Error:
            logger.exception("power_strip_model -> create")

            return False

    def delete(self, device_id):
        """
        Delete power strip by device_id

        :param device_id:
        :return: True | False
        """

        query = """
                DELETE FROM power_strip
                WHERE device_id=%s
                """

        try:
            self.curs.execute(query, (device_id,))
            self.conn.commit()

            return True
        except mysql.Error:
            logger.exception("power_strip_model -> delete")

            return False

    def update_name(self, id, new_name):
        """
        Update name of a specific power strip

        :param id: ID of device
        :param new_name:
        :return: True | False
        """

        query = """
                UPDATE power_strip
                SET name=%s
                WHERE device_id=%s
                """

        try:
            self.curs.execute(query, (new_name, id))
            self.conn.commit()

            return True
        except mysql.Error:
            logger.exception("power_strip_model -> update_name")

            return False

    def update_switch_name(self, id, switch_number, new_name):
        """
        Update name of a specific switch of specific power strip

        :param id: ID of device
        :param switch_number:
        :param new_name:
        :return: True | False
        """

        query = """
                        UPDATE power_strip
                        SET switch_name=%s
                        WHERE device_id=%s AND switch_number=%s
                        """

        try:
            self.curs.execute(query, (new_name, id, switch_number))
            self.conn.commit()

            return True
        except mysql.Error:
            logger.exception("power_strip_model -> update_switch_name")

            return False

    def check_name(self, name):
        """
        Check if name exists into the DB

        :param name:
        :return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT *
                    FROM power_strip
                    WHERE name=%s
                )
                """

        try:
            self.curs.execute(query, (name,))
            res = self.curs.fetchone()
            self.conn.commit()

            return bool(res[0])
        except mysql.Error:
            logger.exception("power_strip_model -> check_name")

            return False

    def get_switch_number(self, id):
        """
        Count how many switch have a specific power strip

        :param id: ID of device
        :return: Number of switchs | False
        """

        query = """
                SELECT COUNT(*)
                FROM power_strip
                WHERE device_id=%s
                """

        try:
            self.curs.execute(query, (id,))
            res = self.curs.fetchone()
            self.conn.commit()

            return res[0]
        except mysql.Error:
            logger.exception("power_strip_model -> get_switch_number")

            return False
