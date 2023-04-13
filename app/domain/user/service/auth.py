from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal

import jwt

from core.base import BaseService
from domain.user.dto.auth import AuthInfo
from domain.user.entity.user import User
from domain.user.exceptions import NotAuthenticatedException


@dataclass
class AuthService(BaseService):
    access_token_expire: timedelta
    refresh_token_expire: timedelta
    jwt_secret: str
    jwt_algorithm: str

    def issue_token(self, user: User, type_: Literal["access", "refresh"]) -> str:
        match type_:
            case "access":
                exp = self.access_token_expire
            case "refresh":
                exp = self.refresh_token_expire
            case _:
                raise ValueError(f'Invalid token type "{type_}"')
        return jwt.encode(
            {
                "sub": user.id,
                "exp": datetime.now() + exp,
                "type": type_,
            },
            self.jwt_secret,
            self.jwt_algorithm,
        )

    def authenticate(self, access_token: str) -> AuthInfo:
        try:
            decoded = jwt.decode(access_token, self.jwt_secret, [self.jwt_algorithm])
        except jwt.InvalidTokenError:
            raise NotAuthenticatedException
        else:
            return AuthInfo(id=decoded["sub"])
