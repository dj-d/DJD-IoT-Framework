import mysql.connector as mariadb
from database.database import Database
from services.logger_service import LoggerService

logging_service = LoggerService(name=__name__)

logger = logging_service.get_logger()


class OctoPrintSchema:
    """
    Provide methods for OctoPrint profile management
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

        self.create_octoprint_table()

    def __del__(self):
        self.conn.close()

    def create_octoprint_table(self):
        """
        Init octoprint table

        :return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS octoprint (
                    ip CHAR(22) NOT NULL UNIQUE,
                    host VARCHAR(255) NOT NULL,
                    x_api_key CHAR(32) NOT NULL UNIQUE PRIMARY KEY
                );
                """

        self.curs.execute(query)
        self.conn.commit()


class OctoPrintModel:
    """
    Provide methods for OctoPrint profile management into the DB
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

    def create(self, ip, host, x_api_key):
        """
        Create new OctoPrint profile

        :param ip: IP of the device with OctoPrint
        :param host: The domain on which to make requests
        :param x_api_key: X_API_KEY of OctoPrint
        :return: True | False
        """

        query = """
                INSERT INTO octoprint(ip, host, x_api_key)
                VALUES (%s, %s, %s)
                """

        try:
            self.curs.execute(query, (ip, host, x_api_key))
            self.conn.commit()

            return True
        except mariadb.Error:
            logger.exception("octoprint_model -> create")

            return False

    def delete(self, x_api_key):
        """
        Delete an OctoPrint profile by x_api_key

        :param x_api_key: X_API_KEY of OctoPrint
        :return: True | False
        """

        query = """
                DELETE FROM octoprint
                WHERE x_api_key=%s
                """

        try:
            self.curs.execute(query, (x_api_key,))
            self.conn.commit()

            return True
        except mariadb.Error:
            logger.exception("octoprint_model -> delete")

            return False
