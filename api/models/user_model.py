from email.policy import default

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.models import common_model_addons as cmn


class User:
    def __init__(self, app, db):
        self.app: Flask = app
        self.db: SQLAlchemy() = db

    def define_model(self):
        class UserModel(self.db.Model, cmn.BaseIDandTableName, cmn.TimestampCreatedMixin, cmn.TimestampLastEditMixin):
            firstname = self.db.Column(self.db.String, nullable=False)
            lastname = self.db.Column(self.db.String, nullable=False)
            email = self.db.Column(self.db.String, unique=True, nullable=False)
            password_hash = self.db.Column(self.db.String, nullable=False)
            is_admin = self.db.Column(self.db.Boolean, nullable=False, default=False)

            def __init__(self, firstname, lastname, email, password_hash, is_admin):
                super().__init__()
                self.firstname = firstname
                self.lastname = lastname
                self.email = email
                self.password_hash = password_hash
                self.is_admin = is_admin

            def to_dict(self, detailed=False):
                # TODO: Move JSON Serialisation related functions to use Marshmallow Schemas
                if detailed:
                    data = {'id': self.id,
                            'firstname': self.firstname,
                            'lastname': self.lastname,
                            'email': self.email,
                            'created_at': str(self.created_at),
                            'last_edit': str(self.last_edit),
                            'is_admin':self.is_admin}
                else:
                    data = {'id': self.id}
                return data

        return UserModel
