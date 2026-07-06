from sqlalchemy import select, insert, update

from app.sql.models.user import User
from app.sql.repo.base import BaseRepository


class UserRepository(BaseRepository):
    async def create_user(
        self, user_id: int, username: str | None, full_name: str, is_admin: bool = False
    ) -> User:
        stmt = (
            insert(User)
            .values(
                id=user_id, username=username, full_name=full_name, is_admin=is_admin
            )
            .returning(User)
        )
        user = await self.session.execute(stmt)
        await self.session.commit()
        return user.scalar_one()

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def set_plan(self, user_id: int, amount: int, account_id: str) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(amount=amount, account_id=account_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def mark_session_used(self, user_id: int) -> None:
        stmt = update(User).where(User.id == user_id).values(session_used=True)
        await self.session.execute(stmt)
        await self.session.commit()
