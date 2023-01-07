from pydantic import BaseModel, Field

from ._internal import BaseConfig

__all__ = ["config", "Config"]


class AppConfig(BaseModel):
    name: str = Field(description="")


class Config(BaseConfig):
    app: AppConfig


config = Config()
