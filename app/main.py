from logging import getLogger

from container import MainContainer
from core.fastapi_ import App


def create_app():
    app = App()

    app.container: MainContainer = MainContainer()
    app.container.check_dependencies()
    app.container.wire()

    from handler.rest import ContextMiddleware, router

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

    return app


app = create_app()
