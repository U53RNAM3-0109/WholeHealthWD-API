from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from unicodedata import category

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
            item_image_64 = self.db.Column(self.db.String, nullable=False)
            item_image_format = self.db.Column(self.db.String, nullable=False)
            item_price = self.db.Column(self.db.String, nullable=False)
            category_id = self.db.Column(self.db.Integer, self.db.ForeignKey('category.id'))

            category = self.db.relationship('CategoryModel', backref='item', uselist=False)


            def __init__(self, image_64, image_format, title, snippet, description, price, category_id):
                super().__init__()
                self.item_image_64 = image_64
                self.item_image_format = image_format
                self.item_title = title
                self.item_snippet = snippet
                self.item_description = description
                self.item_price = price
                self.category_id = category_id

            def to_dict(self, detailed=False):
                if detailed:
                    data = {'id': self.id,
                            'image_64':self.item_image_64,
                            'image_format':self.item_image_format,
                            'title': self.item_title,
                            'snippet': self.item_snippet,
                            'description': self.item_description,
                            'price': self.item_price,
                            'category_id': self.category_id
                            }
                else:
                    data = {'id': self.id}
                return data

        return ItemModel
