from random import randint

from flask_sqlalchemy import SQLAlchemy

from .models import user_model

from flask import Flask
from flask_restful import Api

class BtecBytesAPI(Flask):

    def __init__(self, __name__, db_uri, db_pass):
        super().__init__(__name__)
        self.api = Api(self)
        self.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        self.config["SQLALCHEMY_DATABASE_PASSWORD"] = db_pass

        self.db = SQLAlchemy()
        self.db.init_app(self)

        UserModel = user_model.User(self, self.db)
        self.UserModel = UserModel.defineModel()

        with self.app_context():
            self.db.create_all()

        self.create_routes()

    def create_routes(self):

        @self.route('/userset/<id>')
        def userset(id):
            print("SET")
            user = self.UserModel(id, "email"+str(randint(1,100)), "name"+str(randint(1,100)), "Password"+str(randint(1,100)))
            self.db.session.add(user)
            self.db.session.commit()

            return (f"Something happened for {id}")

        @self.route('/userget/<id>')
        def userget(id):

            user = self.db.get_or_404(self.UserModel, id)

            if user:
                return user.email
            else:
                return "Returned None"
