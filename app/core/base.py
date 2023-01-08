from logging import getLogger, Logger
from typing import ClassVar

from pydantic import BaseModel

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


class BaseRepo(Component):
    type = "repo"
    impl = "base"


class BaseService(Component):
    type = "service"
    impl = "base"
