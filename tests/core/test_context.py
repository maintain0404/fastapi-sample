import pytest

from asyncio import TaskGroup

from app.core.context import _BaseContextExecutor, ContextProperty


class Context(_BaseContextExecutor):
    required: ContextProperty[str] = ContextProperty()
    not_set: ContextProperty[str] = ContextProperty()
    default: ContextProperty[str] = ContextProperty(default="default")
    factory: ContextProperty[str] = ContextProperty(default_factory=lambda: "default")


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
    
