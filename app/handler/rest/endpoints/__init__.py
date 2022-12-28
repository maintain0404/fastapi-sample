from app.core.framework import APIRouter

from .healthcheck import router as healthcheck_router

__all__ = ["router"]


router = APIRouter(prefix="")
router.include_router(healthcheck_router)
