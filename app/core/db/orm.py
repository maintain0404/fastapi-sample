from typing import Any

from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (  # nopycln: import
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
    registry,
)
from sqlalchemy.schema import MetaData
from sqlalchemy.types import TypeEngine

from core.var.config import config
from core.var.context import Context

metadata = MetaData(schema="app")
type_annotation_map: dict[type, TypeEngine] = {}
class_registry: dict[str, Any] = {}
mapper_registry = registry(
    metadata=metadata,
    class_registry=class_registry,
    type_annotation_map=type_annotation_map,
)


engine = create_async_engine(config.db.sqlalchemy_uri)
sessionmaker = async_sessionmaker(engine, expire_on_commit=True)
session: AsyncSession = async_scoped_session(
    session_factory=sessionmaker, scopefunc=Context.id.__get__  # type: ignore[attr-defined]
)  # type: ignore[assignment]


class BaseEntity(MappedAsDataclass, DeclarativeBase, eq=False, order=False):
    registry = mapper_registry
