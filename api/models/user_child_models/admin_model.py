from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.models import common_model_addons as cmn

class Admin:

    def __init__(self, app, db):
        self.app : Flask = app
        self.db : SQLAlchemy() = db

    def define_model(self):
        class AdminModel(self.db.Model, cmn.BaseIDandTableName):
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('user.id'), unique=True)
            access_rank = self.db.Column(self.db.String)

            user = self.db.relationship('UserModel',backref='admin',uselist=False)

            def __init__(self, user_id, access_rank):
                self.user_id = user_id
                self.access_rank = access_rank

            def to_dict(self):
                return {"id":self.id,
                        "user_id":self.user_id,
                        "access_rank":self.access_rank}
        return AdminModel