from flask_sqlalchemy import SQLAlchemy
from flask import Flask

class User:

    def __init__(self, app, db):
        self.app : Flask = app
        self.db : SQLAlchemy() = db

    def defineModel(self):

        class UserModel(self.db.Model):
            __tablename__ = 'users'
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String, nullable=False)
            email = self.db.Column(self.db.String, unique=True, nullable=False)
            password = self.db.Column(self.db.String, nullable=False)

            def __init__(self, id, username, email, password):
                self.id = id
                self.username = username
                self.email = email
                self.password = password

            def __repr__(self):
                return f'<User {self.username}>'

        return UserModel