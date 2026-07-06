from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboards.admin import AMOUNTS, amounts_keyboard, admin_main_menu
from app.sql.repo import Repo
from app.states.admin import GenerateKey
from app.utils.generate_random_key import generate_key

router = Router()


@router.message(F.text == "Generate Key")
async def get_amount(message: Message, state: FSMContext):
    await state.set_state(GenerateKey.amount)
    await message.answer("Выберите сумму для ключа", reply_markup=amounts_keyboard())


@router.message(GenerateKey.amount, F.text.in_({f"{amount}£" for amount in AMOUNTS}))
async def create_key(message: Message, state: FSMContext, repo: Repo):
    amount = int("".join(char for char in message.text if char.isdigit()))  # type: ignore

    key = generate_key(amount)
    await repo.key.create_key(key=key, amount=amount)

    await state.clear()
    await message.answer(
        f"Ключ на {amount}£:\n{key}", reply_markup=ReplyKeyboardRemove()
    )
