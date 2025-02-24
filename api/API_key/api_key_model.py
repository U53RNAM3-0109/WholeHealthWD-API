from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from api.models import common_model_addons as cmn

class ApiKey:

    def __init__(self, db):
        self.db: SQLAlchemy() = db

    def define_model(self):
        class ApiKeyModel(self.db.Model, cmn.BaseIDandTableName, cmn.TimestampCreatedMixin):
            key = self.db.Column(self.db.String, nullable=False)
            expired = self.db.Column(self.db.Boolean, nullalbe=False)

            def __init__(self, uuid=uuid4()):
                super().__init__()
                self.key = uuid
                self.expired = False

        return ApiKeyModel