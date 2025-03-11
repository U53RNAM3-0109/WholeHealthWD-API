import sqlalchemy.exc
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from passlib.hash import pbkdf2_sha512 as sha512


class UserAuthResource(Resource):
    """
    Resource for authenticating user logins.

    :param app: The Flask App implementing the resource.
    """

    def __init__(self, app):
        # We add the parameter, app, so that the Resource can access the DB, models, etc..
        self.app = app
        super().__init__()

    def post(self):
        """
        Takes a supplied email and password, and finds the user the email matches to. Then, if the password hash is
        correct, returns the user ID and 200. Otherwise, returns 401 Unauthorised and no data.

        URL-Argument: "email" - The Email submitted from the login form
        URL-Argument: "password" - The Password submitted from the login form

        :return: Response JSON
        """

        parser = RequestParser()

        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        data = parser.parse_args()

        email = data['email'].lower()

        user = self.app.UserModel.query.filter_by(email=email).first()

        if user:
            check = password_checker(data['password'], user.password_hash)
            if check:
                response = {
                    'response': 200,
                    'data': {'id': user.id},
                    'message': "Login authorised"
                }
                return response
        response = {
            'response': 401,
            'data': None,
            'message': "Unauthorised."
        }
        return response


def password_hasher(pword):
    hash = sha512.hash(pword)

    return hash


def password_checker(pword, hash):
    result = sha512.verify(pword, hash)
    return result
