from contextlib import AbstractAsyncContextManager, AbstractContextManager
from contextvars import Context as StdContext
from contextvars import ContextVar, copy_context, Token
from types import TracebackType
from typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    dataclass_transform,
    Generic,
    Optional,
    Self,
)

from core.annotation import P, T, TV, UNDEFINED, UndefinedType


class _ContextProperty(Generic[TV]):
    cv: ContextVar

    def __init__(
        self,
        default: TV | UndefinedType = UNDEFINED,
        default_factory: Callable[[], TV] | UndefinedType = UNDEFINED,
    ):
        self.default = default
        self.default_factory = default_factory

    def __set_name__(self, owner: type["BaseContext"], name: str) -> None:
        self.cv = ContextVar(name)
        self.name = name

    def __get__(
        self, obj: Optional["BaseContext"], objtype: type["BaseContext"] | None
    ) -> TV:
        return self.cv.get()

    def __set__(self, owner: Optional["BaseContext"], value: TV) -> None:
        if owner:
            owner._tokens[self.name] = self.cv.set(value)
        else:
            raise AttributeError


def context_property(
    default: TV | UndefinedType = UNDEFINED,
    default_factory: Callable[[], TV] | UndefinedType = UNDEFINED,
):
    return _ContextProperty(default=default, default_factory=default_factory)


@dataclass_transform(
    eq_default=False,
    order_default=False,
    kw_only_default=False,
    field_specifiers=(context_property,),
)
class BaseContext(AbstractAsyncContextManager, AbstractContextManager):
    _cvs: ClassVar[dict[str, ContextVar]]
    _attrs: ClassVar[dict[str, _ContextProperty]]
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
            if isinstance(attr, _ContextProperty):
                cls._attrs[name] = attr
                cls._cvs[name] = attr.cv

    def __enter__(
        self,
    ) -> Self:
        return self

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        for token in self._tokens.values():
            token.var.reset(token)
        return None

    async def __aenter__(
        self,
    ) -> Self:
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
