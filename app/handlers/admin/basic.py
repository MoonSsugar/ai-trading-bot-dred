from aiogram import Router, F
from aiogram.types import Message

from app.filters.admin import AdminFilter
from app.keyboards.admin import admin_main_menu
from app.sql.repo import Repo

router = Router()


@router.message(F.text == "/admin", AdminFilter())
async def admin_panel(message: Message, repo: Repo):
    await repo.user.mark_session_used(user_id=message.from_user.id, is_used=False)  # type: ignore

    await message.answer(
        "Добро пожаловать в админ-панель!", reply_markup=admin_main_menu()
    )
