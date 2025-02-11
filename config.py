from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class KeyVaultManager:
    def __init__ (self, vault_uri):
        self.vault_uri = vault_uri
        self.credential = DefaultAzureCredential()

    def get_secret(self, secret_name):
        with SecretClient(vault_url=self.vault_uri, credential=self.credential) as sec_client:
            retr = sec_client.get_secret(secret_name)
        return retr
