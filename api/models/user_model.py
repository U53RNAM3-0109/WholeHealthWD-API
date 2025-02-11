from flask_sqlalchemy import SQLAlchemy

class User:

    def __init__(self, db, username, email, password):
        self.db : SQLAlchemy() = db
        self.username = username
        self.email = email
        self.password = password
        self.id = None

    def create_table(self):
        db = self.db
        class UserModel(self.db.Model):
            __tablename__ = 'users'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String, nullable=False)
            email = db.Column(db.String, unique=True, nullable=False)
            password = db.Column(db.String, nullable=False)

            def __init__(self, username, email, password):
                self.username = username
                self.email = email
                self.password = password

            def __repr__(self):
                return f'<User {self.username}>'

        db.create_all()