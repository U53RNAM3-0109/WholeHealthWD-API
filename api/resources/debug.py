import sqlalchemy.exc
from flask_restful import Api, Resource



class DebugResource(Resource):
    """
    Resource for debugging the API
    """

    def __init__(self, ):
        super().__init__()

    def get(self):
        response = {"response": 200,
                    "data": None,
                    "message": "DEBUG DATA RESPONSE"
                    }
        return response