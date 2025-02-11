from flask import request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from ..models.user_model import User

class UserResource(Resource):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def get(self, user_id):
        user_model = User(self.db, '', '', '')
        UserModel = user_model.create_table()

        user = UserModel.query.get(user_id)
        if user:
            return {
                'id':user.id,
                'username':user.username,
                'email':user.email
            }
        else:
            return {'message':'User not found'}

    def post(self, user_id):
        data = request.get_json()
        user_model = User(self.db, data['username'], data['email'], data['password'])
        UserModel=user_model.create_table()
        new_user = UserModel(username=data['username'],
                             email=data['email'],
                             password=data['password'])