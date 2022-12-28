from typing import ClassVar


class AppException(Exception):
    ...


class ConfigException(AppException):
    ...


class DomainError(AppException):
    status_code: ClassVar[int]
    message: ClassVar[str] | str  # type: ignore[valid-type]
