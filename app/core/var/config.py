from os import environ
from tomllib import load

from pydantic import BaseModel, Field, SecretStr

from ._internal import BaseConfig

__all__ = ["config", "Config"]


def toml_config_settings_source(config: "Config"):
    CONFIG_PATH = environ.get("APP_CONFIG_FILEPATH", "app.toml")
    with open(CONFIG_PATH, mode="rb") as f:
        return load(f)


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

    @property
    def sqlalchemy_uri(self) -> str:
        return (
            f"{self.name}+{self.api}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.path}"
        )


class Config(BaseConfig):
    app: AppConfig
    db: DatabaseConfig

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                toml_config_settings_source,
                env_settings,
                file_secret_settings,
            )


config = Config()  # type: ignore
