from dataclasses import dataclass

import bcrypt

from core.base import BaseService
from domain.user.dto.user_self import (
    ShowMeDto,
    SignInDto,
    SignInSuccessDto,
    SignUpDto,
    SignUpSuccessDto,
)
from domain.user.entity.user import User
from domain.user.exceptions import (
    InvalidPasswordException,
    UserAlreadyExistException,
    UserNotExistException,
)
from domain.user.repo import UserRepo
from domain.user.service.auth import AuthService


@dataclass
class UserSelfService(BaseService):
    repo: UserRepo
    auth: AuthService

    async def sign_in(self, dto: SignInDto) -> SignInSuccessDto:
        user = await self.repo.find_by_email(dto.email)
        if user is None:
            raise UserNotExistException

        # TODO: Remove type: ignore mark after updating pydantic into v2.
        # https://github.com/pydantic/pydantic/blob/main/pydantic/types.py#L536
        if not bcrypt.checkpw(dto.password, user.password):  # type: ignore[arg-type]
            raise InvalidPasswordException

        return SignInSuccessDto(
            id=user.id,
            email=user.email,
            access_token=self.auth.issue_token(user, "access"),
            refresh_token=self.auth.issue_token(user, "refresh"),
        )

    async def sign_up(self, dto: SignUpDto) -> SignUpSuccessDto:
        if await self.repo.find_by_email(dto.email):
            raise UserAlreadyExistException

        # TODO: Remove type: ignore mark after updating pydantic into v2.
        # https://github.com/pydantic/pydantic/blob/main/pydantic/types.py#L536
        hashed_pw: bytes = bcrypt.hashpw(dto.password, bcrypt.gensalt())  # type: ignore[arg-type]
        # TODO: Remove type: ignore mark after mypy fixes bug.
        # https://github.com/sqlalchemy/sqlalchemy/issues/9467
        user = User(email=dto.email, password=hashed_pw)  # type: ignore[arg-type]
        await self.repo.save(user)
        return SignUpSuccessDto.from_orm(user)

    async def show_me(self, user_id: int) -> ShowMeDto:
        user = await self.repo.find_by_id(user_id)
        if user is None:
            raise UserNotExistException

        return ShowMeDto.from_orm(user)
