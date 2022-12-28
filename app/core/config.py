from pydantic import BaseSettings

LOGGING_CONFIG_FILENAME = "logging"

__all__ = ["config", "Config"]


class Config(BaseSettings):
    ...


config = Config()
