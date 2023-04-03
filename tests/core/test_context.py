from asyncio import TaskGroup

import pytest

from core.var.context import BaseContext, context_property


class Context(BaseContext):
    required: str = context_property()
    not_set: str = context_property()
    default: str = context_property(default="default")
    factory: str = context_property(default_factory=lambda: "default")


def test_Context_contextmanager():
    with Context(required="required"):
        assert Context.default == "default"
        assert Context.factory == "default"
        assert Context.required == "required"

        with pytest.raises(LookupError):
            Context.not_set


async def test_Context_run():
    async def fun():
        assert Context.default == "default"
        assert Context.factory == "default"
        assert Context.required == "required"

        with pytest.raises(LookupError):
            Context.not_set

    ctx = Context(required="required")

    ctx.run(fun)

    async with TaskGroup() as tg:
        for _ in range(3):
            await tg.create_task(ctx.run(fun))
