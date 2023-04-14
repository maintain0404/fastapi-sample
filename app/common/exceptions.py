from core.base import AppException


class EntityAlreadyExists(AppException):
    ...


class EntityNotFound(AppException):
    ...


class RelatedEntityNotFound(AppException):
    ...


class RelatedEntityAlreadyExists(AppException):
    ...
