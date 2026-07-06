from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.sql.repo import Repo


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, repo: Repo) -> bool:
        user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
        return user is not None and user.is_admin
