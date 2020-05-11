import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from services.logger_service import LoggerService
import json

logging_service = LoggerService(name=__name__)
logger = logging_service.get_logger()


class EmailService:
    """
    Provide methods for send email to users
    """

    def __init__(self):
        with open('credentials.json') as json_file:
            file = json.load(json_file)
            self.credential = file["email"]

        self.smtp_server = smtplib.SMTP_SSL(host=self.credential["host"], port=self.credential["port"])
        self.smtp_server.ehlo()

        self.local_domain = "localhost"
        self.local_port = "5000"

    def send_message(self, receiver, subject, message):
        """
        Send email to an user with a subject and a message

        :param receiver: The receiver
        :param subject: The subject
        :param message: The message
        :return: Boolean | SMTPException
        """

        try:
            self.smtp_server.login(self.credential["address"], self.credential["password"])

            msg = MIMEMultipart()

            msg["From"] = self.credential["address"]
            msg["To"] = receiver
            msg["Subject"] = subject

            msg.attach(MIMEText(message, 'plain'))

            self.smtp_server.send_message(msg)
            del msg

            self.smtp_server.quit()

            return True
        except smtplib.SMTPException as e:
            logger.exception("email_service -> send_message")

            return False

    def send_otp(self, receiver, otp):
        """
        Send OTP code of the user

        :param receiver: The receiver
        :param otp: The OTP Code
        :return: Boolean | SMTPException
        """

        subject = "RPI-Controller: OTP code"
        msg = "Your verification code for rpi-app is: \n" + str(otp)

        return self.send_message(receiver=receiver, subject=subject, message=msg)

    def send_reset_password(self, receiver):
        """
        Send a link for reset password to a specific user

        :param receiver: The receiver
        :return: Boolean | SMTPException
        """

        change_password_link = self.local_domain + ":" + self.local_port + "/change-password"

        subject = "RPI-Controller: Reset password"

        msg = "Click on the link below to reset your password. \n"
        msg += change_password_link + "\n\n"
        msg += "If it was not you who asked to reset the password, we advise you to contact us."

        return self.send_message(receiver=receiver, subject=subject, message=msg)
