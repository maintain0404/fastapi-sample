from contextlib import AbstractAsyncContextManager, nullcontext

from starlette.types import ASGIApp, Receive, Scope, Send

from core.var.context import Context, RunType

__all__ = ["ContextMiddleware"]


class ContextMiddleware:
    def __init__(self, app: ASGIApp):
        self.app: ASGIApp = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ctx: AbstractAsyncContextManager
        if scope["type"] == "http":
            ctx = Context(runtime=RunType.HTTP)
        elif scope["type"] == "websocket":
            ctx = Context(runtime=RunType.WEBSOCKET)
        else:
            ctx = nullcontext()

        async with ctx:
            await self.app(scope, receive, send)
