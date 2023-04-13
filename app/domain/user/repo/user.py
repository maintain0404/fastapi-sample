from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from core.base import BaseRdbRepo, BaseRepo
from core.db.orm import select
from domain.user.entity import User


@dataclass
class UserRepo(BaseRdbRepo[User]):
    session: AsyncSession

    async def find_by_id(self, id: int) -> User | None:
        return await self.session.get(User, id)

    async def find_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))
