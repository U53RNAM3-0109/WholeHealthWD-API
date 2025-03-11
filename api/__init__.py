from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

from api.models.user_model import User
from api.models.category_model import Category
from api.models.item_model import Item
from api.models.wishlist_model import Wishlist

from .resources import user
from .resources import auth
from .resources import category
from .resources import item
from .resources import wishlist

from flask import Flask
from flask_restful import Api


class WholeHealthAPI(Flask):
    api: Api
    db: SQLAlchemy

    def __init__(self, __name__, db_uri):
        super().__init__(__name__)
        self.WishlistModel = None
        self.UserModel = None
        self.CategoryModel = None
        self.ItemModel = None
        self.api = Api(self)
        self.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        self.db = SQLAlchemy()
        self.db.init_app(self)

        self.define_models()

        with self.app_context():
            self.db.create_all()

        self.api.add_resource(user.UserResource, "/user", resource_class_kwargs={'app': self})
        self.api.add_resource(user.SpecifiedUserResource, "/user/<user_id>", resource_class_kwargs={'app': self})
        self.api.add_resource(auth.UserAuthResource, "/auth", resource_class_kwargs={'app': self})
        self.api.add_resource(category.CategoryResource, "/category", resource_class_kwargs={'app': self})
        self.api.add_resource(category.SpecifiedCategoryResource, "/category/<url_ext>", resource_class_kwargs={'app': self})
        self.api.add_resource(item.ItemResource, "/item", resource_class_kwargs={'app': self})
        self.api.add_resource(item.SpecifiedItemResource, "/item/<item_id>", resource_class_kwargs={'app': self})
        self.api.add_resource(wishlist.WishlistResource, "/wishlist", resource_class_kwargs={'app': self})
        self.api.add_resource(wishlist.SpecifiedWishlistResource, "/wishlist/<wishlist_id>", resource_class_kwargs={'app': self})

        self.api.init_app(self)

    def define_models(self):
        self.UserModel = User(self, self.db).define_model()
        self.ItemModel = Item(self, self.db).define_model()
        self.CategoryModel = Category(self, self.db).define_model()
        self.WishlistModel = Wishlist(self, self.db).define_model()
