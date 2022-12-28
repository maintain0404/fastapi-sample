from contextlib import AbstractAsyncContextManager, nullcontext

import uvicorn
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.context import Context

__all__ = ["ContextMiddleware"]


class ContextMiddleware:
    def __init__(self, app: ASGIApp):
        self.app: ASGIApp = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ctx: AbstractAsyncContextManager
        if scope["type"] == "http":
            ctx = Context(runtime="http")
        elif scope["type"] == "websocket":
            ctx = Context(runtime="websocket")
        else:
            ctx = nullcontext()

        async with ctx:
            await self.app(scope, receive, send)
