from core.fastapi_ import APIRouter

from .account import router as user_router
from .healthcheck import router as healthcheck_router

__all__ = ["router"]


router = APIRouter(prefix="/api")
router.include_router(healthcheck_router)
router.include_router(user_router)
