import sqlalchemy.exc
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser


class CategoryResource(Resource):
    """
    Provides generic resources for creating and reading Categories.

    :param app: The flask app implementing the resource.
    """

    def __init__(self, app):
        # We add an additional parameter, app, so that the Resource can access the DB, models, etc..
        self.app = app
        super().__init__()

    def get(self):
        """
        Provides a list of all Categories in the system.

        URL-Argument: "detailed" (bool). Determines whether full category info is returned, or just ID & title.

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'
        """
        parser = RequestParser()  # init req parser

        # Add arguments. See URL-Argument details above
        parser.add_argument('detailed', type=bool, location='args')

        args = parser.parse_args()  # Parse args from the request

        # Save args into variables
        detailed = args["detailed"]

        # Query for all users
        categories = self.app.CategoryModel.query.all()
        data = []

        for category in categories:
            if detailed:  # If the detailed arg was set to True
                new_data = category.to_dict(detailed)  # Add the category's details

                data.append(new_data)  # Append to list of categories

            else:  # If the detailed arg was False or None
                new_data = category.to_dict()  # Add the Category info to list, undetailed (just ID)

                data.append(category.to_dict())  # Append to the list

        if data:  # If we were able to make a list, return the list and the number found
            response = {
                "response": 200,
                "data": data,
                "message": f"{len(data)} categories(s) found."
            }
            return response
        else:  # If no list was made, return 400 and none.
            response = {
                "response": 400,
                "data": None,
                "message": "No categories found."
            }
            return response

    def post(self):
        """
        Adds new categories to the database and returns the added category's details & ID

        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """
        parser = RequestParser()  # Init req parser

        parser.add_argument('title', type=str)
        parser.add_argument('snippet', type=str)
        parser.add_argument('description', type=str)

        # Parse args from request.
        data = parser.parse_args()
        try:
            data = parser.parse_args()


            # Create a new category
            new_category = self.app.CategoryModel(
                title=data["title"],
                snippet=data["snippet"],
                description=data["description"]
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

        if new_category:  # If a new category was successfully created
            # Add to a dict for response
            data = new_category.to_dict(True)

            response = {
                "response": 200,
                "data": data,
                "message": "Category successfully created"
            }

            return response
        else:
            # If no user was created, for some reason, return a response declaring as such.
            response = {
                "response": 400,
                "data": None,
                "message": "Category not created"
            }
            return response


class SpecifiedCategoryResource(Resource):
    """
    Resource for getting data on a specific category.

    :param app: The Flask app implementing this resource.
    """

    def __init__(self, app):
        # Add App parameter - to access DB, Session, common funcs, etc..
        self.app = app
        super().__init__()

    def get(self, category_id):
        """
        Gets the requested category's data.

        :param category_id: The ID of the category in question
        :return: Response JSON with 'response', 'data', 'message' and possibly 'exception'.
        """
        catgegory = self.app.CategoryModel.query.filter_by(id=category_id).first()

        if catgegory:
            data = catgegory.to_dict(detailed=True)

            response = {
                "response": 200,
                "data": data,
                "message": "Category found."
            }
            return response
        else:
            response = {
                "response": 400,
                "data": None,
                "message": "Category does not exist."
            }
            return response

