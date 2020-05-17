from services.email_service import EmailService
from models.user_model import UserModel

from validate_email import validate_email
from random import randint
import hashlib

from services.logger_service import LoggerService

logging_service = LoggerService(name=__name__)

logger = logging_service.get_logger()


class LoginService:
    """
    Provide methods for login management
    """

    def __init__(self, otp_digits=4):
        self.email = EmailService()

        self.otp_digits = otp_digits
        self.user_model = UserModel()

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

    @staticmethod
    def is_valid_email(email):
        return validate_email(email=email)

    @staticmethod
    def api_key_generator(email, password):
        """
        Create a SHA256 code with tuple(email, password)

        :param email: Email of the user
        :param password: Password of the user
        :return: SHA256 code
        """

        hash_string = email + password + email.split('@')[0]
        sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()

        return sha_signature

    def user_exists(self, email, api_key):
        """
        Check if a user exists into the DB

        :param email:
        :param api_key:
        :return: True | False
        """

        if self.is_valid_email(email):
            return self.user_model.check_user(email, api_key)
        else:
            logger.error("login_service -> user_exists")

            return False

    def create_user(self, name, surname, username, email, password):
        """
        Create a user by

        :param name:
        :param surname:
        :param username:
        :param email:
        :param password:
        :return: api_key | False
        """

        if name and surname and username and email and password:
            if self.is_valid_email(email) and not self.user_model.check_username(username):
                api_key = self.api_key_generator(email, password)

                if not self.user_exists(email, api_key):
                    return self.make_response(True, {'api_key': self.user_model.create(name, surname, username, email, api_key)}, 200)

        return self.make_response(False, "Not valid input", 400)

    def user_logged(self, email, api_key, otp_code):
        """
        Get a specific user by

        :param email:
        :param api_key:
        :param otp_code:
        :return: True | False
        """

        if self.is_valid_email(email):
            if self.user_model.get_user_with_otp(email, api_key, otp_code) and self.clear_otp(api_key, otp_code):
                self.user_model.reset_otp_requests(api_key)

                return True

            return False
        else:
            logger.error("login_service -> user_logged")

            return False

    # TODO: To improve
    def send_reset_password(self, email, password):
        """
        Send email for reset password

        :param email:
        :param password:
        :return: True | False
        """

        if self.is_valid_email(email):
            if self.user_model.check_user(email, self.api_key_generator(email, password)):  # TODO: This condition is not perfect
                return self.email.send_reset_password(email)
        else:
            logger.error("login_service -> send_reset_password")

            return False

    @staticmethod
    def generate_otp():
        """
        Create a random OTP of 6 digits

        :return: OTP code
        """

        return randint(100000, 999999)

    def send_otp_code(self, email, api_key):
        """
        Send OTP code via email

        :param email:
        :param api_key:
        :return: True | False
        """

        if self.is_valid_email(email) and self.user_exists(email, api_key):
            otp_code = self.generate_otp()
            self.user_model.create_otp(api_key, otp_code)

            if self.check_otp_requests(email, api_key, otp_code):
                timestamp = self.user_model.get_otp_timestamp(api_key)
                otp_requests = self.user_model.get_otp_requests(api_key) + 1

                self.user_model.update_otp(otp_requests, timestamp, api_key)

                if self.email.send_otp(email, otp_code):
                    return True
        else:
            logger.error("login_service -> send_otp_code")

        return False

    def clear_otp(self, api_key, otp_code):
        """
        Delete OTP code after login
        
        :param api_key: api_key of user that logged in
        :param otp_code: OTP code of user that logged in
        :return: True | False
        """

        return self.user_model.delete_otp(api_key, otp_code)

    def check_otp_requests(self, email, api_key, otp_code):
        """
        Check if the requested limit of otp has been reached

        :param email:
        :param api_key:
        :param otp_code:
        :return: True | False
        """
        if self.user_model.check_user_otp_timestamp(api_key):
            self.user_model.reset_otp_requests(api_key)

        if 0 <= self.user_model.get_otp_requests(api_key) <= 3 and self.user_model.get_user_with_otp(email, api_key, otp_code):
            return True

        return False

    def check_api_key(self, api_key):
        """
        Find user by:

        :param api_key:
        :return True | False
        """

        return self.user_model.check_api_key(api_key)
