from typing import Any

from sqlalchemy.orm import (  # nopycln: import
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
    registry,
)
from sqlalchemy.schema import MetaData
from sqlalchemy.types import TypeEngine

metadata = MetaData(schema="app")
type_annotation_map: dict[type, TypeEngine] = {}
class_registry: dict[str, Any] = {}
mapper_registry = registry(
    metadata=metadata,
    class_registry=class_registry,
    type_annotation_map=type_annotation_map,
)


class BaseEntity(MappedAsDataclass, DeclarativeBase, eq=False, order=False):
    registry = mapper_registry
