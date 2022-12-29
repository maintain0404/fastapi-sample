from contextlib import AbstractAsyncContextManager, AbstractContextManager
from contextvars import Context as StdContext
from contextvars import ContextVar, copy_context, Token
from enum import StrEnum
from types import TracebackType
from typing import Any, Callable, cast, ClassVar, dataclass_transform, Generic, Optional
from uuid import UUID, uuid4

from util.annotation import P, T, TV, UNDEFINED, UndefinedType

__all__ = ["Context", "RunType"]


class ContextProperty(Generic[TV]):
    cv: ContextVar

    def __init__(
        self,
        default: TV | UndefinedType = UNDEFINED,
        default_factory: Callable[[], TV] | UndefinedType = UNDEFINED,
    ):
        self.default = default
        self.default_factory = default_factory

    def __set_name__(self, owner: type["Context"], name: str) -> None:
        self.cv = ContextVar(name)
        self.name = name

    def __get__(self, obj: Optional["Context"], objtype: type["Context"] | None) -> TV:
        return self.cv.get()

    def __set__(self, owner: Optional["Context"], value: TV) -> None:
        if owner:
            owner._tokens[self.name] = self.cv.set(value)
        else:
            raise AttributeError


@dataclass_transform(
    eq_default=False,
    order_default=False,
    kw_only_default=False,
    field_specifiers=(ContextProperty,),
)
class _BaseContextExecutor(AbstractAsyncContextManager, AbstractContextManager):
    _cvs: ClassVar[dict[str, ContextVar]]
    _attrs: ClassVar[dict[str, ContextProperty]]
    _ctx: StdContext
    _tokens: dict[str, Token]

    def __init__(self, **kwargs):
        self._ctx = copy_context()
        self._tokens = {}
        self._fill_defaults(kwargs)
        for k, v in kwargs.items():
            cv = self._cvs[k]
            self._tokens[cv] = cv.set(v)

    def _fill_defaults(self, input: dict[str, Any]):
        for name, attr in self._attrs.items():
            if input.get(name, UNDEFINED) is UNDEFINED:
                if attr.default is not UNDEFINED:
                    input[name] = attr.default
                elif attr.default_factory is not UNDEFINED:
                    input[name] = cast(Callable[[], Any], attr.default_factory)()

    def __init_subclass__(cls) -> None:
        cls._cvs = {}
        cls._attrs = {}
        for name, attr in vars(cls).items():
            if isinstance(attr, ContextProperty):
                cls._attrs[name] = attr
                cls._cvs[name] = attr.cv

    def __enter__(
        self,
    ) -> "_BaseContextExecutor":  # TODO: Change to Self when mypy supports Self
        return self

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        for k, token in self._tokens.items():
            token.var.reset(token)
        return None

    async def __aenter__(
        self,
    ) -> "_BaseContextExecutor":  # TODO: Change to Self when mypy supports Self
        return self

    async def __aexit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        return self.__exit__(__exc_type, __exc_value, __traceback)

    def run(self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return self._ctx.run(func, *args, **kwargs)


class RunType(StrEnum):
    HTTP = "http"
    WEBSOCKET = "websocket"
    BACKGROUND = "background"


class Context(_BaseContextExecutor):
    runtime: ContextProperty[RunType] = ContextProperty(default=RunType.HTTP)
    id: ContextProperty[UUID] = ContextProperty(default_factory=uuid4)
