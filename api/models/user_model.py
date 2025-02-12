from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.models import common_model_addons as cmn

class User:

    def __init__(self, app, db):
        self.app : Flask = app
        self.db : SQLAlchemy() = db

    def define_model(self):
        class UserModel(self.db.Model, cmn.BaseIDandTableName, cmn.TimestampCreatedMixin, cmn.TimestampLastEditMixin):
            username = self.db.Column(self.db.String, nullable=False)
            email = self.db.Column(self.db.String, unique=True, nullable=False)
            password = self.db.Column(self.db.String, nullable=False)

            def __init__(self, username, email, password):
                super().__init__()
                self.username = username
                self.email = email
                self.password = password

            def to_dict(self):
                #TODO: Move JSON Serialisation related functions to use Marshmallow Schemas
                data = {'id':self.id,
                        'username':self.username,
                        'email':self.email,
                        'password':self.password,
                        'created_at':str(self.created_at),
                        'last_edit':str(self.last_edit)}
                return data

        return UserModel