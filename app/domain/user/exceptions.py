from core.base import AppException


class UserDomainException(AppException):
    ...


class UserAlreadyExistException(UserDomainException):
    code = "USR-0001"


class UserNotExistException(UserDomainException):
    code = "USR-0002"


class InvalidPasswordException(UserDomainException):
    code = "USR-0003"


class NotAuthenticatedException(UserDomainException):
    code = "USR-0004"
