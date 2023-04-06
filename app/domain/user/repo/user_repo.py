from core.base import BaseRepo
from core.db.orm import select, session
from domain.user.entity import User


class UserRepo(BaseRepo[User]):
    async def find_by_id(self, id: int) -> User | None:
        return await session.get(User, id)

    async def find_by_email(self, email: str) -> User | None:
        return await session.scalar(select(User).where(User.email == email))
