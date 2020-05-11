import mysql.connector as mariadb
from database.database import Database
from services.logger_service import LoggerService

logging_service = LoggerService(name=__name__)

logger = logging_service.get_logger()


class UserSchema:
    """
    Provide methods for user data management
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

        self.create_user_table()
        self.create_otp_table()

    def __del__(self):
        """
        Body of destructor

        :return: void
        """

        self.conn.close()

    def create_user_table(self):
        """
        Init user table

        :return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS user (
                    name VARCHAR(50) NOT NULL, 
                    surname VARCHAR(50) NOT NULL,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    api_key CHAR(64) NOT NULL UNIQUE PRIMARY KEY,
                    admin TINYINT NOT NULL DEFAULT 0, 
                    created_on DATE DEFAULT (CURRENT_DATE),
                    otp_requests INT DEFAULT 0,
                    last_otp_timestamp TIMESTAMP NULL 
                );
                """

        self.curs.execute(query)
        self.conn.commit()

    def create_otp_table(self):
        """
        Init otp table

        :return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS otp (
                    api_key CHAR(64) NOT NULL UNIQUE PRIMARY KEY, 
                    otp_code INT(6) NOT NULL,
                    otp_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (api_key)
                        REFERENCES user(api_key)
                        ON DELETE CASCADE 
                );
                """

        self.curs.execute(query)
        self.conn.commit()


class UserModel:
    """
    Provide methods for user management into the DB
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

    def create(self, name: str, surname: str, username: str, email: str, api_key: str):
        """
        Create new user.

        :param name:
        :param surname:
        :param username:
        :param email:
        :param api_key:
        :return: api_key | False
        """

        query = """
                INSERT INTO user(name, surname, username, email, api_key)
                VALUES (%s, %s, %s, %s, %s)
                """

        try:
            self.curs.execute(query, (name, surname, username, email, api_key))
            self.conn.commit()

            return api_key
        except mariadb.Error:
            logger.exception("user_model -> create")

            return False

    # TODO
    def delete(self):
        pass

    def update_otp(self, otp_requests, otp_timestamp, api_key):
        query = """
                UPDATE user
                SET otp_requests=%s, last_otp_timestamp=%s
                WHERE api_key=%s
                """

        try:
            self.curs.execute(query, (otp_requests, otp_timestamp, api_key))
            self.conn.commit()

            return True
        except mariadb.Error:
            logger.exception("user_model -> update_otp")

            return False

    def reset_otp_requests(self, api_key):
        query = """
                UPDATE user
                SET otp_requests=0
                WHERE api_key=%s
                """

        try:
            self.curs.execute(query, (api_key,))
            self.conn.commit()

            return True
        except mariadb.Error:
            logger.exception("user_model -> reset_otp_requests")

            return False

    def get_otp_requests(self, api_key):
        query = """
                SELECT otp_requests
                FROM user 
                WHERE api_key=%s
                """

        try:
            self.curs.execute(query, (api_key,))
            res = self.curs.fetchone()
            self.conn.commit()

            return res[0]
        except mariadb.Error:
            logger.exception("user_model -> get_otp_requests")

            return False

    def check_user(self, email: str, api_key: str):
        """
        Find user by:

        :param email:
        :param api_key:
        :returns tuple(email, api_key) | False
        """

        query = """
                SELECT EXISTS (
                    SELECT *
                    FROM user
                    WHERE email=%s AND api_key=%s
                )
                """

        try:
            self.curs.execute(query, (email, api_key))
            res = self.curs.fetchone()
            self.conn.commit()

            return bool(res[0])
        except mariadb.Error:
            logger.exception("user_model -> check_user")

            return False

    def check_username(self, username: str):
        """
        Check if username already exists

        :param username:
        :return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT *
                    FROM user 
                    WHERE username=%s
                )
                """

        try:
            self.curs.execute(query, (username,))
            res = self.curs.fetchone()
            self.conn.commit()

            return bool(res[0])
        except mariadb.Error:
            logger.exception("user_model -> check_username")

            return False

    def check_api_key(self, api_key: str):
        """
        Find user by:

        :param api_key:
        :return True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT * 
                    FROM user
                    WHERE api_key=%s
                    )
                """

        try:
            self.curs.execute(query, (api_key,))
            res = self.curs.fetchone()
            self.conn.commit()

            return bool(res[0])
        except mariadb.Error:
            logger.exception("user_model -> check_api_key")

            return False

    def get_user_with_otp(self, email, api_key, otp):
        """
        Find user by:

        :param email:
        :param api_key:
        :param otp:
        :return: True | False
        """

        # NOTE: "SELECT EXISTS" -> Not work
        query = """
                SELECT user.email, user.api_key, otp.otp_code
                FROM user INNER JOIN otp ON otp.api_key = user.api_key
                WHERE user.email=%s AND user.api_key=%s AND otp.otp_code=%s
                AND otp.otp_timestamp >= NOW() - INTERVAL 15 MINUTE
                """

        try:
            self.curs.execute(query, (email, api_key, otp))
            res = self.curs.fetchone()
            self.conn.commit()

            if res is not None:
                return True

            return False
        except mariadb.Error:
            logger.exception("user_model -> get_user_with_otp")

            return False

    def create_otp(self, api_key: str, otp_code: int):
        """
        Store new otp code.

        :param api_key:
        :param otp_code:
        :return: True | False
        """

        query = """
                REPLACE INTO otp(api_key, otp_code)
                VALUES (%s, %s)
                """

        try:
            self.curs.execute(query, (api_key, otp_code))
            self.conn.commit()

            return True
        except mariadb.Error:
            logger.exception("user_model -> create_otp")

            return False

    def delete_otp(self, api_key: str, otp_code: int):
        """
        Store new otp code.

        :param api_key:
        :param otp_code:
        :return: True | False
        """

        query = """
                DELETE FROM otp 
                WHERE api_key=%s AND otp_code=%s
                """

        try:
            self.curs.execute(query, (api_key, otp_code))
            self.conn.commit()

            return True
        except mariadb.Error:
            logger.exception("user_model -> delete_otp")

            return False

    def get_otp_timestamp(self, api_key):
        query = """
                SELECT otp_timestamp
                FROM otp
                WHERE api_key=%s
                """

        try:
            self.curs.execute(query, (api_key,))
            res = self.curs.fetchone()
            self.conn.commit()

            return res[0]
        except mariadb.Error:
            logger.exception("user_model -> get_otp_info")

            return False
