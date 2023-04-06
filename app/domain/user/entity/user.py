from dataclasses import dataclass

from core.base import BaseEntity
from core.db.mixins import TimestampAuditing
from core.db.types import intpk, required_bytes, required_str


@dataclass
class User(BaseEntity, TimestampAuditing):
    __tablename__ = "user"
    id: intpk
    email: required_str
    password: required_bytes
