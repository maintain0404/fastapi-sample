from datetime import datetime, timedelta
from typing import Literal

import bcrypt
import jwt

from core.base import BaseService
from domain.user.dto.user_self_dto import (
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


class UserSelfService(BaseService):
    repo: UserRepo
    ACCESS_TOKEN_EXP: timedelta
    REFRESH_TOKEN_EXP: timedelta
    JWT_SECRET: str
    JWT_ALGORITHM: str

    def _issue_token(self, user: User, type_: Literal["access", "refresh"]) -> str:
        match type_:
            case "access":
                exp = self.ACCESS_TOKEN_EXP
            case "refresh":
                exp = self.REFRESH_TOKEN_EXP
            case _:
                raise ValueError(f'Invalid token type "{type_}"')
        return jwt.encode(
            {
                "sub": user.id,
                "exp": datetime.now() + exp,
                "type": type_,
            },
            self.JWT_SECRET,
            self.JWT_ALGORITHM,
        )

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
            access_token=self._issue_token(user, "access"),
            refresh_token=self._issue_token(user, "refresh"),
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

    async def authenticate(self, access_token: str) -> bool:
        try:
            jwt.decode(access_token, self.JWT_SECRET, [self.JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            return False
        else:
            return True

    async def show_me(self, user_id: int) -> ShowMeDto:
        user = await self.repo.find_by_id(user_id)
        if user is None:
            raise UserNotExistException

        return ShowMeDto.from_orm(user)
