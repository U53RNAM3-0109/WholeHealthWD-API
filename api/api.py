import models
import resources
import schemas

from flask import Flask
from flask_restful import Api

class BtecBytesAPI(Flask):

    def __init__(self, __name__, db_uri, db_pass):
        super().__init__(__name__)
        self.api = Api(self)

    def attach_resources(self):
        # self.add_resource(res, url, endpoint='', kwargs={})
        pass
