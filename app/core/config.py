from pydantic import BaseModel, Field

from ._internal import BaseConfig

__all__ = ["config", "Config"]


class AppConfig(BaseModel):
    name: str = Field("name", description="")


class Config(BaseConfig):
    app: AppConfig


# Automatically inject parameters from env.
config = Config()  # type: ignore
