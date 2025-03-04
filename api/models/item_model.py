from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.models import common_model_addons as cmn


class Item:
    def __init__(self, app, db):
        self.app: Flask = app
        self.db: SQLAlchemy() = db

    def define_model(self):
        class ItemModel(self.db.Model, cmn.BaseIDandTableName):
            item_title = self.db.Column(self.db.String, nullable=False)
            item_snippet = self.db.Column(self.db.String, nullable=False)
            item_description = self.db.Column(self.db.String, nullable=False)
            item_price = self.db.Column(self.db.Int, nullable=False)

            def __init__(self, title, snippet, description, price):
                super().__init__()
                self.item_title = title
                self.item_snippet = snippet
                self.item_description = description
                self.item_price = price

            def to_dict(self, detailed=False):
                if detailed:
                    data = {'id': self.id,
                            'title': self.title,
                            'snippet': self.snippet,
                            'description': self.description,
                            'price': self.item_price}
                else:
                    data = {'id': self.id}
                return data

        return ItemModel
