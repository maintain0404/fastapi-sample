from enum import StrEnum
from uuid import UUID, uuid4

from ._internal import BaseContext, ContextProperty

__all__ = ["Context", "RunType"]


class RunType(StrEnum):
    HTTP = "http"
    WEBSOCKET = "websocket"
    BACKGROUND = "background"


class Context(BaseContext):
    runtime: ContextProperty[RunType] = ContextProperty(default=RunType.HTTP)
    id: ContextProperty[UUID] = ContextProperty(default_factory=uuid4)
