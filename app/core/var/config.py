from datetime import date, datetime, timedelta
from os import environ

from pydantic import BaseModel, Field, root_validator, SecretStr
from tomllib import load

from ._internal import BaseConfig

__all__ = ["config", "Config"]


class AppConfig(BaseModel):
    name: str = Field("name", description="")


class DatabaseConfig(BaseModel):
    name: str
    api: str
    user: str
    password: SecretStr
    host: str
    port: int
    path: str


class JwtConfig(BaseModel):
    access_token_expire: timedelta
    refresh_token_expire: timedelta
    secret: SecretStr
    algorithm: str = "HS256"


class Config(BaseConfig):
    app: AppConfig
    db: DatabaseConfig
    jwt: JwtConfig


config = Config()  # type: ignore
