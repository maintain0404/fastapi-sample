from functools import partial
from json import load as json_load
from pathlib import Path
from typing import Any, no_type_check

from pydantic import BaseSettings
from pydantic.env_settings import DotenvType, env_file_sentinel, StrPath
from tomllib import load as toml_load
from yaml import FullLoader  # type: ignore[import]
from yaml import load as yaml_load  # type: ignore[import]

from core.base import ConfigException

CONFIG_FILE_NAME = "app"


def get_config_filepath(suffix: str):
    return CONFIG_FILE_NAME + "." + suffix


@no_type_check
def load_configfile() -> dict[str, Any]:
    yaml_loader = partial(yaml_load, loader=FullLoader)
    for path, loader in [
        (get_config_filepath("toml"), toml_load),
        (get_config_filepath("yaml"), yaml_loader),
        (get_config_filepath("yml"), yaml_loader),
        (get_config_filepath("json"), json_load),
    ]:
        if Path(path).is_file():
            with open(path, "r") as f:
                return loader(f)
    raise ConfigException("Config file not found")


class BaseConfig(BaseSettings):
    def __init__(
        __pydantic_self__,
        _env_file: DotenvType | None = env_file_sentinel,
        _env_file_encoding: str | None = None,
        _env_nested_delimiter: str | None = None,
        _secrets_dir: StrPath | None = None,
        **values: Any,
    ) -> None:  # Expose signaure. Copied from pydantic.BaseSettings.__init__
        super().__init__(
            **__pydantic_self__._build_values(
                values,
                _env_file=_env_file,
                _env_file_encoding=_env_file_encoding,
                _env_nested_delimiter=_env_nested_delimiter,
                _secrets_dir=_secrets_dir,
            )
        )

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
                load_configfile,
                env_settings,
                file_secret_settings,
            )
