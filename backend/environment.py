from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    cookie_secret: str

    commerzbank_api_client_id: str
    commerzbank_api_client_secret: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_environment() -> Environment:
    return Environment()