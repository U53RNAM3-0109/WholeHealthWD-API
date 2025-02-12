from flask import request, Flask
from flask_restful import Api, Resource
import json


class UserResource(Resource):
    def __init__(self, app):
        self.app = app
        super().__init__()

    def get(self):
        users = self.app.UserModel.query.all()
        data = []
        for user in users:
            data.append(user.to_dict())

        if data:
            return data
        else:
            return {'message': 'No users found'}

    def post(self):
        req = request.get_json()
        data = json.loads(req)

        try:
            new_user = self.app.UserModel(
                username=data["username"],
                email=data["email"],
                password=data["password"])

            self.app.db.session.add(new_user)
            self.app.db.session.commit()
        except Exception as exc:
            print(exc)
            return "Error occurred, see console"

        if new_user:
            return new_user.to_dict()
        else:
            return "Returned None"


class SpecifiedUserResource(Resource):
    def __init__(self, app):
        self.app = app
        super().__init__()

    def get(self, user_id):
        user = self.app.db.get_or_404(self.app.UserModel, user_id)

        if user:
            return user.to_dict()
        else:
            return {'message': 'User not found'}
