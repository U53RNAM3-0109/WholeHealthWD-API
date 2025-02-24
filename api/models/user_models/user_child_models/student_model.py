from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.models import common_model_addons as cmn


class Student:

    def __init__(self, db):
        self.db: SQLAlchemy() = db

    def define_model(self):
        class StudentModel(self.db.Model, cmn.BaseIDandTableName):
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('user.id'), unique=True)

            user = self.db.relationship('UserModel', backref='student', uselist=False)

            def __init__(self, user_id):
                self.user_id = user_id

            def to_dict(self):
                return {"id": self.id,
                        "user_id": self.user_id}
        return StudentModel