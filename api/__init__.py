from flask_sqlalchemy import SQLAlchemy

from .models import user_model
from .resources import user

from flask import Flask
from flask_restful import Api


class BtecBytesAPI(Flask):
    api: Api
    db: SQLAlchemy

    def __init__(self, __name__, db_uri):
        super().__init__(__name__)
        self.api = Api(self)
        self.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        self.db = SQLAlchemy()
        self.db.init_app(self)

        UserModel = user_model.User(self, self.db)
        self.UserModel = UserModel.define_model()

        with self.app_context():
            self.db.create_all()

        self.api.add_resource(user.UserResource, "/user", resource_class_kwargs={'app': self})
        self.api.add_resource(user.SpecifiedUserResource, "/user/<user_id>", resource_class_kwargs={'app': self})

        self.api.init_app(self)

