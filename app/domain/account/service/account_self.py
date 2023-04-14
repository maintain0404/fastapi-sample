from dataclasses import dataclass

import bcrypt

from core.base import BaseService
from domain.account.dto.account_self import (
    ShowMeDto,
    SignInDto,
    SignInSuccessDto,
    SignUpDto,
    SignUpSuccessDto,
)
from domain.account.entity.account import Account
from domain.account.exceptions import (
    AccountAlreadyExist,
    AccountNotExist,
    InvalidPassword,
)
from domain.account.repo import AccountRepo
from domain.account.service.auth import AuthService


@dataclass
class AccountSelfService(BaseService):
    repo: AccountRepo
    auth: AuthService

    async def sign_in(self, dto: SignInDto) -> SignInSuccessDto:
        account = await self.repo.find_by_email(dto.email)
        if account is None:
            raise AccountNotExist

        # TODO: Remove type: ignore mark after updating pydantic into v2.
        # https://github.com/pydantic/pydantic/blob/main/pydantic/types.py#L536
        if not bcrypt.checkpw(dto.password, account.password):  # type: ignore[arg-type]
            raise InvalidPassword

        return SignInSuccessDto(
            id=account.id,
            email=account.email,
            access_token=self.auth.issue_token(account, "access"),
            refresh_token=self.auth.issue_token(account, "refresh"),
        )

    async def sign_up(self, dto: SignUpDto) -> SignUpSuccessDto:
        if await self.repo.find_by_email(dto.email):
            raise AccountAlreadyExist

        # TODO: Remove type: ignore mark after updating pydantic into v2.
        # https://github.com/pydantic/pydantic/blob/main/pydantic/types.py#L536
        hashed_pw: bytes = bcrypt.hashpw(dto.password, bcrypt.gensalt())  # type: ignore[arg-type]
        # TODO: Remove type: ignore mark after mypy fixes bug.
        # https://github.com/sqlalchemy/sqlalchemy/issues/9467
        account = Account(email=dto.email, password=hashed_pw)  # type: ignore[arg-type]
        await self.repo.save(account)
        return SignUpSuccessDto.from_orm(account)

    async def show_me(self, user_id: int) -> ShowMeDto:
        account = await self.repo.find_by_id(user_id)
        if account is None:
            raise AccountNotExist

        return ShowMeDto.from_orm(account)
