#from config import KeyVaultManager

from api import BtecBytesAPI

app = BtecBytesAPI(__name__, 'sqlite:///test.db')
app.run(debug=True)
