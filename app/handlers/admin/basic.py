from aiogram import Router, F
from aiogram.types import Message

from app.filters.admin import AdminFilter
from app.keyboards.admin import admin_main_menu

router = Router()


@router.message(F.text == "/admin", AdminFilter())
async def admin_panel(message: Message):
    await message.answer(
        "Добро пожаловать в админ-панель!", reply_markup=admin_main_menu()
    )
