from logging import getLogger, Logger
from typing import ClassVar, Generic

from pydantic import BaseModel

from core.annotation import TV

from .db import AsyncSession, BaseEntity  # nopycln


class BaseDTO(BaseModel):
    class Config:
        use_enum_values = True
        orm_mode = True


class Component:
    logger: ClassVar[Logger]
    impl: ClassVar[str]
    type: ClassVar[str]

    def __new__(cls, *args, **kwargs) -> "Component":
        cls.logger.debug(
            f"Component {cls.__name__}(type='{cls.type}' name='{cls.__name__}') created."
        )
        return super().__new__(cls)

    def __init_subclass__(cls) -> None:
        cls.logger = getLogger(f"app.{cls.type}.{cls.__name__}")


class BaseRepo(Generic[TV], Component):
    type = "repo"

    async def save(self, entity: TV):
        ...


class BaseRdbRepo(BaseRepo[TV]):
    session: AsyncSession

    async def save(self, entity: TV) -> TV:
        await self.session.merge(entity)
        return entity


class BaseService(Component):
    type = "service"


# BaseException is python superclass of all exceptions.
# Because of ame conflict with BaseException, use AppException instead.
class AppException(Exception):
    code: ClassVar[str]


class ConfigException(AppException):
    ...
