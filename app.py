from api import BtecBytesAPI

if __name__ == "__main__":
    # App is being run directly, consider this a development environment

    app = BtecBytesAPI(__name__, 'sqlite:///test.db')
    app.run(debug=True)
else:
    # App is being run as app.py, having been imported by another program
    # Consider this the production environment of the Azure API Server.

    from config import KeyVaultManager
    from os import environ

    keyvault_uri = environ.get("keyvault_uri")
    keyvault = KeyVaultManager(vault_uri=keyvault_uri)

    db_uri = keyvault.get_secret("api-db-uri")

    app = BtecBytesAPI(__name__, db_uri)
