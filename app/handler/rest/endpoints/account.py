from fastapi import APIRouter, Response

from core.di import inject
from domain.account.dto.account_self import SignInDto, SignInSuccessDto, SignUpDto
from handler.rest.depends.account import AccountSelfService, AuthInfo

router = APIRouter(prefix="/account")


@router.post("/sign_in", response_model=SignInSuccessDto)
@inject
async def sign_in(
    res: Response,
    dto: SignInDto,
    service: AccountSelfService,
) -> Response:
    sign_in_res = await service.sign_in(dto)
    res.headers["Authorization"] = "Bearer " + sign_in_res.access_token
    res.set_cookie("refresh-token", sign_in_res.refresh_token, httponly=True)

    return res


@router.post("/sign_up")
@inject
async def sign_up(obj: SignUpDto, service: AccountSelfService):
    return await service.sign_up(obj)


@router.get("/me")
@inject
async def show_me(auth_info: AuthInfo, service: AccountSelfService):
    return await service.show_me(auth_info.id)
