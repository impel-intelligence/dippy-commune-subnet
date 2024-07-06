from pydantic_settings import BaseSettings
from config import settings


class ValidatorSettings(BaseSettings):
    # == Scoring ==
    iteration_interval: int = 800  # Set, accordingly to your tempo.
    max_allowed_weights: int = 400  # Query dynamically based on your subnet settings.
    foo: int | None = None  # Anything else that you wish to implement.
    # testnet_uid = 27
    # testnet_registry_key = "5Exsj2WLrVqAeoRKPKGKmAX3HCsiPwb4LNy6975xCJUKWMp7"
    # testnet_registry_url = "35.182.195.207"
    default_key: str = settings.testnet_registry_key
    default_url: str = settings.testnet_registry_url
    default_port: int = 9769
    default_uid: int = settings.testnet_uid
