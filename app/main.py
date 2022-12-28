from logging import getLogger

from app.core.framework import App
from app.handler.rest import router, ContextMiddleware


app = App()

app.include_router(router)
app.add_middleware(ContextMiddleware)


@app.on_event("startup")
async def startup():
    logger = getLogger("app.server")
    logger.info("Startup")


@app.on_event("shutdown")
async def shutdown():
    logger = getLogger("app.server")
    logger.info("Shutdown")
