from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from core.base import BaseRdbRepo, BaseRepo
from core.db.orm import select
from domain.account.entity import Account


@dataclass
class AccountRepo(BaseRdbRepo[Account]):
    session: AsyncSession

    async def find_by_id(self, id: int) -> Account | None:
        return await self.session.get(Account, id)

    async def find_by_email(self, email: str) -> Account | None:
        return await self.session.scalar(select(Account).where(Account.email == email))
