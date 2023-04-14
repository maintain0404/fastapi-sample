from common.exceptions import EntityAlreadyExists
from core.base import AppException


class AccountDomainException(AppException):
    ...


class AccountAlreadyExist(AccountDomainException, EntityAlreadyExists):
    code = "USR-0001"


class AccountNotExist(AccountDomainException, EntityAlreadyExists):
    code = "USR-0002"


class InvalidPassword(AccountDomainException):
    code = "USR-0003"


class NotAuthenticated(AccountDomainException):
    code = "USR-0004"
