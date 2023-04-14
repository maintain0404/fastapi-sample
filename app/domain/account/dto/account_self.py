from pydantic import SecretBytes

from core.base import BaseDTO


class SignInDto(BaseDTO):
    email: str
    password: SecretBytes


class SignInSuccessDto(BaseDTO):
    id: int
    email: str
    access_token: str
    refresh_token: str


class SignUpDto(BaseDTO):
    email: str
    password: SecretBytes


class SignUpSuccessDto(BaseDTO):
    id: int
    email: str


class ShowMeDto(BaseDTO):
    id: int
    email: str
