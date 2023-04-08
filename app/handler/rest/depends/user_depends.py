from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends, Header, HTTPException, status

from container import MainContainer
from domain.user.dto.auth_dto import AuthInfo as AuthInfo_
from domain.user.service.auth_service import AuthService
from domain.user.service.user_self_service import UserSelfService as UserSelfService_


def authenticate(
    service: AuthService = Depends(Provide[MainContainer.auth_service], use_cache=True),
    authorization: str = Header(...),
) -> AuthInfo_:
    scheme, token = authorization.split()
    if scheme.lower() == "bearer":
        return service.authenticate(token)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


AuthInfo = Annotated[AuthInfo_, Depends(authenticate)]
UserSelfService = Annotated[
    UserSelfService_, Depends(Provide[MainContainer.user_self_service])
]
