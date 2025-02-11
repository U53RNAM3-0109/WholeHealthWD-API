#from api import api
#from config import KeyVaultManager
import os

from api.api import BtecBytesAPI

app = BtecBytesAPI(__name__, 'sqlite:///test.db', None)
app.run(debug=True)
