import sqlalchemy.exc
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from .auth import password_hasher


class UserResource(Resource):
    """
    Provides generic resources for creating and reading Users.

    :param app: The flask app implementing the resource.
    """

    def __init__(self, app):
        # We add an additional parameter, app, so that the Resource can access the DB, models, etc..
        self.app = app
        super().__init__()

    def get(self):
        """
        Provides a list of all Users in the system.

        URL-Argument: "detailed" (bool). Determines whether full user info is returned, or just ID & user type.

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'
        """
        parser = RequestParser()  # init req parser

        # Add arguments. See URL-Argument details above
        parser.add_argument('detailed', type=bool, location='args')

        args = parser.parse_args()  # Parse args from the request

        # Save args into variables
        detailed = args["detailed"]

        # Query for all users
        users = self.app.UserModel.query.all()
        data = []

        for user in users:
            if detailed:  # If the detailed arg was set to True
                new_data = user.to_dict(detailed)  # Add the user's details

                data.append(new_data)  # Append to list of users

            else:  # If the detailed arg was False or None
                new_data = user.to_dict()  # Add the User info to list, undetailed (just ID)

                data.append(user.to_dict())  # Append to the list

        if data:  # If we were able to make a list, return the list and the number found
            response = {
                "response": 200,
                "data": data,
                "message": f"{len(data)} user(s) found."
            }
            return response
        else:  # If no list was made, return 400 and none.
            response = {
                "response": 400,
                "data": None,
                "message": "No users found."
            }
            return response

    def post(self):
        """
        Adds new users to the database and returns the added user's details & ID

        URL-Argument: "firstname" (str). First name
        URL-Argument: "lastname" (str). Last name
        URL-Argument: "email" (str). Email (Unique)
        URL-Argument: "password" (str). Password
        URL-Argument: "usertype" (str). Either 'Admin' or 'Customer'.

        The Usertype given determines additional possible columns

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """

        parser = RequestParser()  # Init req parser

        # Add args for URL. See above for details
        parser.add_argument('firstname', type=str)
        parser.add_argument('lastname', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('is_admin', type=bool, required=True)

        # Parse args from request. We don't care if extra args have been given (ie user subtype specific attributes)
        data = parser.parse_args(strict=False)
        try:
            data = parser.parse_args()

            pass_hash = password_hasher(data['password'])
            # Create a new user
            new_user = self.app.UserModel(
                firstname=data['firstname'],
                lastname=data['lastname'],
                email=data['email'].lower(),
                password_hash=pass_hash,
                is_admin=data['is_admin']
            )

            print("COMMIT")
            self.app.db.session.add(new_user)
            self.app.db.session.commit()

        except sqlalchemy.exc.IntegrityError as exc:
            print("INTEG CANCELLED")
            # In  the case of an Integrity error, such as from UNIQUE constraint violation in Email.

            # Return a response detailing as such.
            response = {
                "response": 400,
                "data": None,
                "exception": "INTEGRITY",
                "message": "IntegrityError exception occurred. This may be due to violating UNIQUE constraint, "
                           "such as on the Email field. See 'Exception' for more info."
            }

            # Then roll back the session to last commit
            self.app.db.session.rollback()

            return response

        except Exception as exc:
            print("UNKN CANCELLED")

            # In the case of an unknown exception, we return the details of it and print to the Python console.
            print(exc)

            response = {
                "response": 500,
                "data": None,
                "exception": exc,
                "message": "Unhandled exception occurred, see 'exception' for more information."
            }

            # As before, we roll back the session to the last commit
            self.app.db.session.rollback()

            return response

        if new_user:  # If a new user was successfully created
            # Add to a dict for response
            data = new_user.to_dict(True)

            response = {
                "response": 200,
                "data": data,
                "message": "User successfully created"
            }
            print("USER MADE?")

            return response
        else:
            # If no user was created, for some reason, return a response declaring as such.
            response = {
                "response": 400,
                "data": None,
                "message": "User not created"
            }
            return response


class SpecifiedUserResource(Resource):
    """
    Resource for getting data on a specific user.

    :param app: The Flask app implementing this resource.
    """

    def __init__(self, app):
        # Add App parameter - to access DB, Session, common funcs, etc..
        self.app = app
        super().__init__()

    def post(self, user_id):
        """
        Gets the requested user's data.

        :param user_id: The ID of the User in question
        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """
        user = self.app.UserModel.query.filter_by(id=user_id).first()

        if user:
            data = user.to_dict(detailed=True)

            response = {
                "response": 200,
                "data": data,
                "message": "User found."
            }
            return response
        else:
            response = {
                "response": 400,
                "data": None,
                "message": "User does not exist."
            }
            return response

