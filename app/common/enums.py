from enum import Enum

from .datastructures import Permission


class AuthScope(Permission, Enum):
    """Available Oauth2 scopes."""

    SIGNIN = ("signin", "Need sign in")

    @classmethod
    def scope_dict(cls) -> dict:
        return {v.name: v.description for v in cls.__members__.values()}
