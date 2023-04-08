from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
    registry,
)
from sqlalchemy.schema import MetaData
from sqlalchemy.types import TypeEngine

from core.var.config import config, Config
from core.var.context import Context

metadata = MetaData(schema="app")
type_annotation_map: dict[type, TypeEngine] = {}
class_registry: dict[str, Any] = {}
mapper_registry = registry(
    metadata=metadata,
    class_registry=class_registry,
    type_annotation_map=type_annotation_map,
)


class BaseEntity(
    MappedAsDataclass, DeclarativeBase, eq=False, order=False, kw_only=True
):
    registry = mapper_registry


async def get_session(sessionmaker: async_sessionmaker):
    async with sessionmaker.begin() as session:
        yield session


def build_sa_uri(
    name: str, api: str, user: str, password: str, host: str, port: str, path: str
) -> str:
    return f"{name}+{api}://{user}:{password}@{host}:{port}/{path}"


async def check_conn(engine: AsyncEngine):
    conn = await engine.connect()
