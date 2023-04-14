from sqlalchemy.orm import Mapped, mapped_column

from core.base import BaseEntity
from core.db.mixins import TimestampAuditing
from core.db.types import intpk


class Account(BaseEntity, TimestampAuditing):
    __tablename__ = "account"
    id: Mapped[intpk] = mapped_column(init=False)
    email: Mapped[str] = mapped_column()
    password: Mapped[bytes] = mapped_column()
