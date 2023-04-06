from datetime import datetime

from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column


@declarative_mixin
class TimestampAuditing:
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
