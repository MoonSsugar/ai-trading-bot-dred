from sqlalchemy import insert, select, update

from app.sql.models.key import Key
from app.sql.repo.base import BaseRepository


class KeyRepository(BaseRepository):
    async def create_key(self, key: str, amount: int) -> Key:
        stmt = insert(Key).values(key=key, amount=amount).returning(Key)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_key_by_key(self, key: str) -> Key | None:
        stmt = select(Key).where(Key.key == key)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_key_as_used(self, key: str) -> None:
        stmt = update(Key).where(Key.key == key).values(is_used=True)
        await self.session.execute(stmt)
        await self.session.commit()
