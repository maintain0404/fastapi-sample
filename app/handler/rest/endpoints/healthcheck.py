from app.core.framework import APIRouter, JSONResponse

HELATH_RESPONSE = JSONResponse({"message": "Ok"})
router = APIRouter(prefix="/health")


@router.get("")
def healthcheck():
    return HELATH_RESPONSE
