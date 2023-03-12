from enum import StrEnum
from uuid import UUID, uuid4

from ._internal import BaseContext, context_property

__all__ = ["Context", "RunType"]


class RunType(StrEnum):
    HTTP = "http"
    WEBSOCKET = "websocket"
    BACKGROUND = "background"


class Context(BaseContext):
    runtime: RunType = context_property(default=RunType.HTTP)
    id: UUID = context_property(default_factory=uuid4)
