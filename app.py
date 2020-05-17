from flask import Flask, jsonify, request
from waitress import serve

from models.device_model import DeviceSchema
from models.octoprint_model import OctoPrintSchema
from models.user_model import UserSchema

from services.login_service import LoginService
from services.device_service import DeviceService

DOMAIN = "djd-server.ddns.net"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return "It working..."


@app.route("/signup", methods=["POST"])
def signup():
    credential = request.get_json(force=True)

    if "name" in credential and "surname" in credential and "username" in credential and "email" in credential and "password" in credential:
        res = LoginService().create_user(credential["name"], credential["surname"], credential["username"], credential["email"], credential["password"])

        return make_response(res["valid"], res["info"], res["code"])
    else:
        return make_response(False, "Not valid input", 400)


@app.route("/otp_request", methods=["POST"])
def otp_request():
    credential = request.get_json(force=True)

    if "email" in credential and "api_key" in credential:
        email = credential['email']
        api_key = credential['api_key']

        login_service = LoginService()

        if login_service.user_exists(email, api_key):
            if login_service.send_otp_code(email, api_key):
                return make_response(True, "Email send", 200)
            return make_response(False, "Error when send OTP code", 500)
        return make_response(False, "Not valid user", 400)
    else:
        return make_response(False, "Not valid input", 400)


@app.route("/login", methods=["POST"])
def login():
    credential = request.get_json(force=True)
    email = credential['email']
    api_key = credential['api_key']
    otp_code = credential['otp']

    if "email" in credential and "api_key" in credential and "otp" in credential:
        login_service = LoginService()

        if login_service.user_logged(email, api_key, otp_code):
            return make_response(True, "User logged", 200)
        else:
            login_service.clear_otp(api_key, otp_code)

            return make_response(False, "Not valid user", 400)
    else:
        return make_response(False, "Not valid input", 400)


@app.route("/change_password", methods=["POST"])
def change_password():
    # TODO
    pass


@app.route("/reset_password", methods=["GET"])
def reset_password():
    # TODO
    pass


@app.route("/device", methods=["POST"])
def device():
    data = request.get_json(force=True)

    if LoginService().check_api_key(data["api_key"]):
        res = DeviceService().manager(data)

        if res["valid"]:
            return make_response(True, res["info"], res['code'])

        return make_response(False, res["info"], res['code'])

    return make_response(False, "Not valid API KEY", 400)


def make_response(is_valid, info, error_code):
    """
    Make response for the client

    :param is_valid: The success of the operation
    :param info: Some information
    :param error_code: HTMl error code
    :return: JSON
    """

    return jsonify({'valid': is_valid, 'info': info}), error_code


if __name__ == "__main__":
    DeviceSchema()
    OctoPrintSchema()
    UserSchema()

    app.run(host='0.0.0.0', debug=True)  # For development
    # serve(app, port=5000, threads=6)
