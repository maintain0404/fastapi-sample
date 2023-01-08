import pytest

from core.db import BaseEntity, Mapped, mapped_column


class Sample(BaseEntity):
    __tablename__ = "sample"
    pk: Mapped[int] = mapped_column(primary_key=True)


def test_BaseEntity():
    s1 = Sample(pk=1)
    s2 = Sample(pk=1)
    s3 = Sample(pk=2)

    with pytest.raises(TypeError):
        sorted([s1, s2, s3])

    assert not s1 == s2
    assert not s1 == s3
