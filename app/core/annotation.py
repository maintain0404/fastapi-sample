from typing import ParamSpec, TypeVar

T = TypeVar("T")
TV = TypeVar("TV")
TV1 = TypeVar("TV1")
TV2 = TypeVar("TV2")
TV3 = TypeVar("TV3")


class UndefinedType:
    ...


UNDEFINED = UndefinedType()


P = ParamSpec("P")
