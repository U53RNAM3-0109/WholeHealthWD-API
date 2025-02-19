import sqlalchemy.exc
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser


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
        URL-Argument: "whitelist" (string). Filters to only return the specified user type. ('Student', 'Teacher',
        'Admin')
        URL-Argument: "blacklist" (string). Filters to return everything but the specified user type. ('Student',
        'Teacher', 'Admin')

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'
        """
        parser = RequestParser()  # init req parser

        # Add arguments. See URL-Argument details above
        parser.add_argument('detailed', type=bool, location='args')
        parser.add_argument("whitelist", type=str, location='args')
        parser.add_argument("blacklist", type=str, location='args')

        args = parser.parse_args()  # Parse args from the request

        # Save args into variables
        detailed = args["detailed"]
        type_whitelist = args["whitelist"]
        type_blacklist = args["blacklist"]

        # Query for all users
        users = self.app.UserModel.query.all()
        data = []

        for user in users:
            child, child_type = get_user_child(self.app, user.id)  # Get the type of user (student/teacher/admin)
            if type_matches(child_type, type_whitelist, type_blacklist):  # If the user type fits the filters
                if detailed:  # If the detailed arg was set to True
                    new_data = user.to_dict(detailed)  # Add the user's details
                    if child:  # If the user has a subtype of user attached
                        new_data.update(child.to_dict(detailed))  # Add the sub-user details as well

                    data.append(new_data)  # Append to list of users

                else:  # If the detailed arg was False or None
                    new_data = user.to_dict()  # Add the User info to list, undetailed (just ID)
                    if child:  # If a subtype of user was found
                        new_data["usertype"] = child_type  # Add the usertype as well.

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
        URL-Argument: "password" (str). Password hash
        URL-Argument: "usertype" (str). Either 'Admin', 'Student' or 'Teacher'.

        The Usertype given determines additional possible columns

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """
        parser = RequestParser()  # Init req parser

        # Add args for URL. See above for details
        parser.add_argument('firstname', type=str)
        parser.add_argument('lastname', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('usertype', type=str, required=True)

        # Parse args from request. We don't care if extra args have been given (ie user subtype specific attributes)
        data = parser.parse_args(strict=False)
        try:
            # Get user's type and add the type specific attributes, if any, to the arg list
            usertype = data['usertype']
            if usertype == 'Student':
                pass
            elif usertype == 'Teacher':
                pass
            elif usertype == 'Admin':
                parser.add_argument('accessrank', type=str)
            else:
                # If the usertype isn't accepted, raise ValueError
                raise ValueError(f"Usertype {usertype} is not accepted for arg 'usertype'.")

            # Parse additional args as added by type
            data = parser.parse_args()

            # Create a new user
            new_user = self.app.UserModel(
                firstname=data['firstname'],
                lastname=data['lastname'],
                email=data['email'],
                password=data['password'])

            # Create the provided user type record, then add both to the session
            if usertype == 'Student':
                new_student = self.app.StudentModel(
                    user_id=new_user.id,
                )
                self.app.db.session.add(new_user, new_student)

            elif usertype == 'Teacher':
                new_teacher = self.app.StudentModel(
                    user_id=new_user.id,
                )
                self.app.db.session.add(new_user, new_teacher)

            elif usertype == 'Admin':
                new_admin = self.app.AdminModel(
                    user_id=new_user.id,
                    access_rank=data['accessrank']
                )
                self.app.db.session.add(new_user, new_admin)

            else:
                # If the usertype isn't valid, we should have already raised ValueError,
                # but we need a fallback just in case.
                # i.e. A usertype option has been added, but the model hasn't been made yet.
                raise ValueError(f"User type {usertype} is not an available model.")
            self.app.db.session.commit()

        except sqlalchemy.exc.IntegrityError as exc:
            # In  the case of an Integrity error, such as from UNIQUE constraint violation in Email.

            # Return a response detailing as such.
            response = {
                "response": 400,
                "data": None,
                "exception": exc,
                "message": "IntegrityError exception occurred. This may be due to violating UNIQUE constraint, "
                           "such as on the Email field. See 'Exception' for more info."
            }

            # Then roll back the session to last commit
            self.app.db.session.rollback()

            return response

        except Exception as exc:
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
            # Get the user's child & child type
            child, child_type = get_user_child(self.app, new_user.id)
            # Add both to the response data and return.
            data = new_user.to_dict(True)
            if child:
                data.update(child.to_dict(True))

            response = {
                "response": 200,
                "data": data,
                "message": "User successfully created"
            }

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

    def get(self, user_id):
        """
        Gets the requested user's data.

        :param user_id: The ID of the User in question
        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """
        user = self.app.UserModel.query.filter_by(id=user_id).first()

        if user:
            data = user.to_dict(detailed=True)
            child, child_type = get_user_child(self.app, user.id)

            if child:
                data.update(child.to_dict(detailed=True))

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


def get_user_child(app, user_id):
    """
    Helper function to get the User's type and the relevant record.

    :param app: The current flask app, to provide context for DB models
    :param user_id: The ID of the user in
    question. This should be the ID of the User table, not the admin/student/teacher table.
    :return: The child record and type of user, or None if none found.
    """

    # Get all records of Student, Teacher or Admin that match the user's id.
    # Only one should be returned, as we disallow a user from having multiple user types.
    student = app.StudentModel.query.filter_by(user_id=user_id).first()
    teacher = app.TeacherModel.query.filter_by(user_id=user_id).first()
    admin = app.AdminModel.query.filter_by(user_id=user_id).first()

    # If somehow multiple are found, we return the type with the lowest access rank (Student, then Teacher, then Admin)
    if student:
        return student, "student"
    if teacher:
        return teacher, "teacher"
    if admin:
        return admin, "admin"

    # If a user doesn't have a child type, we return None.
    return None, None


def type_matches(users_type, whitelist=(), blacklist=()):
    """
    Helper function to determine whether a user's type fits in the given filter.
    At time of writing, only 3 user types exist. If the type does not fit with either list, False is returned.
    No errors are raised if the given lists contradict, for now.

    :param users_type: The user's type.
    :param whitelist: A type whitelist, as a list/tuple
    :param blacklist: A type blacklist, as a list/tuple
    :return: True if the User satisfies both white and blacklist, False if the user catches either of them.
    """

    # Default to True
    is_valid = True

    # If a blacklist is present, and the user type is in the list, turn is_valid to False
    if blacklist and users_type in blacklist:
        is_valid = False

    # If a whitelist is present, and the user type is not in the list, turn is_valid to False
    if whitelist and users_type not in whitelist:
        is_valid = False

    # Then return is_valid
    return is_valid
