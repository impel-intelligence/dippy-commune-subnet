from communex.module.client import ModuleClient
from communex.types import Ss58Address

from config import settings


class RegistryClient:
    def __init__(self, keypair, use_testnet=False):
        client = ModuleClient(
            settings.testnet_registry_url, settings.registry_port, keypair
        )
        if use_testnet:
            client = ModuleClient(
                settings.testnet_registry_url, settings.registry_port, keypair
            )
        self.client = client
        self.destination_key = Ss58Address(settings.testnet_registry_key)

    def module_client(self):
        return self.client
