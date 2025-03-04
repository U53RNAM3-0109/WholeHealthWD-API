import sqlalchemy.exc
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser


class ItemResource(Resource):
    """
    Provides generic resources for creating and reading Items.

    :param app: The flask app implementing the resource.
    """

    def __init__(self, app):
        # We add an additional parameter, app, so that the Resource can access the DB, models, etc..
        self.app = app
        super().__init__()

    def get(self):
        """
        Provides a list of all Items in the system.

        URL-Argument: "detailed" (bool). Determines whether full item info is returned, or just ID & title.

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'
        """
        parser = RequestParser()  # init req parser

        # Add arguments. See URL-Argument details above
        parser.add_argument('detailed', type=bool, location='args')

        args = parser.parse_args()  # Parse args from the request

        # Save args into variables
        detailed = args["detailed"]

        # Query for all users
        items = self.app.ItemModel.query.all()
        data = []

        for item in items:
            if detailed:  # If the detailed arg was set to True
                new_data = item.to_dict(detailed)  # Add the item's details

                data.append(new_data)  # Append to list of items

            else:  # If the detailed arg was False or None
                new_data = item.to_dict()  # Add the Item info to list, undetailed (just ID)

                data.append(item.to_dict())  # Append to the list

        if data:  # If we were able to make a list, return the list and the number found
            response = {
                "response": 200,
                "data": data,
                "message": f"{len(data)} items(s) found."
            }
            return response
        else:  # If no list was made, return 400 and none.
            response = {
                "response": 400,
                "data": None,
                "message": "No items found."
            }
            return response

    def post(self):
        """
        Adds new items to the database and returns the added item's details & ID

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """
        parser = RequestParser()  # Init req parser

        # Parse args from request.
        data = parser.parse_args()
        try:
            data = parser.parse_args()


            # Create a new item
            new_item = self.app.ItemModel(

            )

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

        if new_item:  # If a new item was successfully created
            # Add to a dict for response
            data = new_item.to_dict(True)

            response = {
                "response": 200,
                "data": data,
                "message": "Item successfully created"
            }

            return response
        else:
            # If no user was created, for some reason, return a response declaring as such.
            response = {
                "response": 400,
                "data": None,
                "message": "Item not created"
            }
            return response


class SpecifiedItemResource(Resource):
    """
    Resource for getting data on a specific item.

    :param app: The Flask app implementing this resource.
    """

    def __init__(self, app):
        # Add App parameter - to access DB, Session, common funcs, etc..
        self.app = app
        super().__init__()

    def get(self, item_id):
        """
        Gets the requested item's data.

        :param item_id: The ID of the item in question
        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """
        user = self.app.UserModel.query.filter_by(id=user_id).first()

        if user:
            data = user.to_dict(detailed=True)

            response = {
                "response": 200,
                "data": data,
                "message": "Item found."
            }
            return response
        else:
            response = {
                "response": 400,
                "data": None,
                "message": "Item does not exist."
            }
            return response

