from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message, ReplyKeyboardRemove

from app.keyboards.admin import AMOUNTS, amounts_keyboard
from app.sql.repo import Repo
from app.states.admin import GenerateKey
from app.utils.generate_random_key import generate_key

router = Router()

# Upper bound so a typo like "100000" can't lock up the bot / hit Telegram limits.
MAX_KEYS = 500
# Telegram's hard limit for a text message.
TELEGRAM_MAX_CHARS = 4096


@router.message(F.text == "Generate Key")
async def get_amount(message: Message, state: FSMContext):
    await state.set_state(GenerateKey.amount)
    await message.answer("Выберите сумму для ключа", reply_markup=amounts_keyboard())


@router.message(GenerateKey.amount, F.text.in_({f"{amount}£" for amount in AMOUNTS}))
async def get_count(message: Message, state: FSMContext):
    amount = int("".join(char for char in message.text if char.isdigit()))  # type: ignore
    await state.update_data(amount=amount)
    await state.set_state(GenerateKey.count)
    await message.answer(
        "Сколько ключей вы хотите создать?", reply_markup=ReplyKeyboardRemove()
    )


@router.message(GenerateKey.count, F.text)
async def create_keys(message: Message, state: FSMContext, repo: Repo):
    raw = message.text.strip()  # type: ignore
    if not raw.isdigit() or int(raw) == 0:
        await message.answer("Введите положительное целое число")
        return

    count = int(raw)
    if count > MAX_KEYS:
        await message.answer(f"Слишком много. Максимум {MAX_KEYS} ключей за раз")
        return

    data = await state.get_data()
    amount = data["amount"]

    # Generate unique keys, de-duplicating within the batch so the unique
    # constraint on `key` can't fail against another key from this same run.
    keys: list[str] = []
    seen: set[str] = set()
    while len(keys) < count:
        key = generate_key(amount)
        if key not in seen:
            seen.add(key)
            keys.append(key)

    await repo.key.create_keys(keys, amount)
    await state.clear()

    header = f"Ключи на {amount}£ ({count} шт.):"
    body = "\n".join(keys)
    text = f"{header}\n{body}"

    # One message when it fits; otherwise a single .txt file (still in order).
    if len(text) <= TELEGRAM_MAX_CHARS:
        await message.answer(text)
    else:
        document = BufferedInputFile(body.encode("utf-8"), filename=f"keys_{amount}.txt")
        await message.answer_document(document, caption=header)
