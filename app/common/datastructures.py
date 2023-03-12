from typing import Self


class Permission(str):
    """Represents OAuth2 scope."""

    description: str

    def __new__(cls, name: str, description: str) -> Self:
        obj = super().__new__(cls, name)
        obj.description = description
        return obj

    def __init__(self, name: str, description: str) -> None:  # expose signature
        super().__init__()
