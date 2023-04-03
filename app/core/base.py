from logging import getLogger, Logger
from typing import ClassVar, Generic

from pydantic import BaseModel

from util.annotation import TV

from .db import BaseEntity  # nopycln


class BaseDTO(BaseModel):
    class Config:
        use_enum_values = True


class Component:
    logger: ClassVar[Logger]
    impl: ClassVar[str]
    type: ClassVar[str]

    def __new__(cls) -> "Component":
        cls.logger.debug(f"Component {cls.__name__}({cls.type=} {cls.impl=}) created.")
        return super().__new__(cls)

    def __init_subclass__(cls) -> None:
        cls.logger = getLogger(f"app.{cls.type}.{cls.impl}")


class BaseRepo(Component, Generic[TV]):
    type = "repo"
    impl = "base"

    async def save(self, entity: TV):
        ...


class BaseService(Component):
    type = "service"
    impl = "base"


# BaseException is python superclass of all exceptions.
# Because of ame conflict with BaseException, use AppException instead.
class AppException(Exception):
    ...


class ConfigException(AppException):
    ...
