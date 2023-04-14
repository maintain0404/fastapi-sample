from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends, Header, HTTPException, status

from container import MainContainer
from domain.account.dto.auth import AuthInfo as AuthInfo_
from domain.account.service.account_self import AccountSelfService as UserSelfService_
from domain.account.service.auth import AuthService


def authenticate(
    service: AuthService = Depends(Provide[MainContainer.auth_service], use_cache=True),
    authorization: str = Header(...),
) -> AuthInfo_:
    scheme, token = authorization.split()
    if scheme.lower() == "bearer":
        return service.authenticate(token)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"www-authenticate": "bearer"},
        )


AuthInfo = Annotated[AuthInfo_, Depends(authenticate)]
AccountSelfService = Annotated[
    UserSelfService_, Depends(Provide[MainContainer.account_self_service])
]
