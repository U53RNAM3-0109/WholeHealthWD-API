from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from unicodedata import category

from api.models import common_model_addons as cmn

class Category:
    def __init__(self, app, db):
        self.app: Flask = app
        self.db: SQLAlchemy() = db

    def define_model(self):
        app = self.app
        class CategoryModel(self.db.Model, cmn.BaseIDandTableName):
            category_title = self.db.Column(self.db.String, nullable=False)
            category_url_ext = self.db.Column(self.db.String, nullable=False, unique=True)
            category_image = self.db.Column(self.db.String, nullable=False)
            category_image_format = self.db.Column(self.db.String, nullable=False)
            category_snippet = self.db.Column(self.db.String, nullable=False)
            category_description = self.db.Column(self.db.String, nullable=False)

            def __init__(self, category_title, category_snippet, category_description, category_image_64, category_image_format, category_url_ext):
                super().__init__()
                self.category_title = category_title
                self.category_snippet = category_snippet
                self.category_description = category_description
                self.category_image =category_image_64
                self.category_image_format = category_image_format
                self.category_url_ext = category_url_ext

            def to_dict(self, detailed=False):
                if detailed:
                    items = app.ItemModel.query.all()

                    item_data = []

                    for item in items:
                        print(f"found item: {item.item_title}")
                        if item.category_id == self.id:
                            item_data.append(item.to_dict(detailed=True))

                    data = {'id': self.id,
                            'title': self.category_title,
                            'snippet': self.category_snippet,
                            'description': self.category_description,
                            'image_64':self.category_image,
                            'image_format':self.category_image_format,
                            'cat_items':item_data,
                            'url_ext':self.category_url_ext
                            }
                else:
                    data = {'id': self.id, 'title':self.category_title, 'url_ext':self.category_url_ext}
                return data

        return CategoryModel
