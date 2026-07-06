from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.user import main_menu_kb
from app.menu import MAIN_MENU, MENU_FOOTER, account_summary
from app.sql.repo import Repo
from app.states.user import Activation

router = Router()

START_MESSAGE = """Welcome to Nebula AI. The next generation of AI-powered trading 🌐\n
Nebula AI analyses the market, identifies trading opportunities and executes trading sessions using intelligent automation — helping you save time and trade smarter\n
🚀 To get started, enter your activation code below and follow the instructions inside the platform """

INVALID_CODE_MESSAGE = (
    "❌ Invalid activation code\n\n"
    "We couldn't find this code in our system. "
    "Please double-check it and try again."
)


def build_activation_message(account_id: str, amount: int) -> str:
    return (
        "✅ Access Activated\n\n"
        "Your Nebula AI access has been successfully activated\n\n"
        + account_summary(account_id, amount)
        + "\n\n"
        + MENU_FOOTER
    )


@router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext, repo: Repo):
    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    if user is None:
        first_name = message.from_user.first_name or ""  # type: ignore
        last_name = message.from_user.last_name or ""  # type: ignore
        full_name = f"{first_name} {last_name}".strip()

        await repo.user.create_user(
            user_id=message.from_user.id,  # type: ignore
            username=message.from_user.username,  # type: ignore
            full_name=full_name,
        )
    # Expect an activation code next; only then does check_code respond.
    await state.set_state(Activation.code)
    await message.answer(START_MESSAGE)


@router.message(Activation.code, F.text)
async def check_code(message: Message, state: FSMContext, repo: Repo):
    code = message.text.strip()  # type: ignore

    key = await repo.key.get_key_by_key(code)
    if key is None or key.is_used:
        await message.answer(INVALID_CODE_MESSAGE)
        return

    # Account ID is the 8 digits contained in the activation key.
    account_id = "".join(char for char in code if char.isdigit())

    # Persist the plan and account id so the menu can be rebuilt after the key
    # is consumed.
    await repo.user.set_plan(message.from_user.id, key.amount, account_id)  # type: ignore

    await message.answer(
        build_activation_message(account_id, key.amount),
        reply_markup=main_menu_kb(),
    )
    await repo.key.mark_key_as_used(code)

    # Activation done: stop treating messages as codes, seed nav at the main menu.
    await state.set_state(None)
    await state.update_data(nav_stack=[MAIN_MENU])
