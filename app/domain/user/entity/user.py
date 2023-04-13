from sqlalchemy.orm import Mapped, mapped_column

from core.base import BaseEntity
from core.db.mixins import TimestampAuditing
from core.db.types import intpk


class User(BaseEntity, TimestampAuditing):
    __tablename__ = "user"
    id: Mapped[intpk] = mapped_column(init=False)
    email: Mapped[str] = mapped_column()
    password: Mapped[bytes] = mapped_column()
