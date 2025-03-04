from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.models import common_model_addons as cmn


class Wishlist:
    def __init__(self, app, db):
        self.app: Flask = app
        self.db: SQLAlchemy() = db

    def define_model(self):
        class WishlistModel(self.db.Model, cmn.BaseIDandTableName, cmn.TimestampCreatedMixin, cmn.TimestampLastEditMixin):
            wishlist_title = self.db.Column(self.db.String, nullable=False)
            wishlist_snippet = self.db.Column(self.db.String, nullable=False)
            wishlist_description = self.db.Column(self.db.String, nullable=False)
            item_id = self.db.Column(self.db.Integer, self.db.ForeignKey('item.id'), unique=True)
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('user.id'), unique=True)

            item = self.db.relationship('ItemModel', backref='wishlist', uselist=False)
            user = self.db.relationship('UserModel', backref='wishlist', uselist=False)

            def __init__(self, item_id, user_id):
                super().__init__()
                self.item_id = item_id
                self.user_id = user_id

            def to_dict(self, detailed=False):
                if detailed:
                    data = {'id': self.id,
                            'item_id': self.category_id,
                            'item_name': self.item.name,
                            'item_snippet': self.item.snippet,
                            'item_price': self.item.price,
                            'user_id': self.category_id,
                            'last_edit': self.last_edit,
                            'created_at': self.created_at
                            }
                else:
                    data = {'id': self.id}
                return data

        return WishlistModel
