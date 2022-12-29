from logging import getLogger

from core.fastapi_ import App
from handler.rest import ContextMiddleware, router

app = App()

app.include_router(router)
app.add_middleware(ContextMiddleware)


@app.on_event("startup")
async def startup():
    logger = getLogger("app.server")
    logger.info("Application start up.")


@app.on_event("shutdown")
async def shutdown():
    logger = getLogger("app.server")
    logger.info("Application shutdown.")
