from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.models import common_model_addons as cmn


class Category:
    def __init__(self, app, db):
        self.app: Flask = app
        self.db: SQLAlchemy() = db

    def define_model(self):
        class CategoryModel(self.db.Model, cmn.BaseIDandTableName):
            category_title = self.db.Column(self.db.String, nullable=False)
            category_snippet = self.db.Column(self.db.String, nullable=False)
            category_description = self.db.Column(self.db.String, nullable=False)

            def __init__(self, title, snippet, description):
                super().__init__()
                self.category_title = title
                self.category_snippet = snippet
                self.category_description = description

            def to_dict(self, detailed=False):
                if detailed:
                    data = {'id': self.id,
                            'title': self.title,
                            'snippet': self.snippet,
                            'description': self.description}
                else:
                    data = {'id': self.id}
                return data

        return CategoryModel
