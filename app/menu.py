"""Simple screen-based navigation with a dynamic Back button.

Each "screen" knows how to render itself (text + keyboard). The screens the
user has visited are kept as a stack in the FSM data (`nav_stack`). Going
forward pushes a screen; the single Back handler just pops one screen and
re-renders whatever is now on top — so one handler covers every Back button,
no matter how many screens exist.
"""

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.user import (
    back_kb,
    main_menu_kb,
    post_session_kb,
    session_kb,
    withdraw_method_kb,
)
from app.sql.repo import Repo

# Screen ids.
MAIN_MENU = "main_menu"
SESSION = "session"
HISTORY = "history"
WITHDRAW = "withdraw"

# Maps a key amount to its (access plan, start balance) values.
PLANS: dict[int, tuple[str, str]] = {
    80: ("Starter Trial", "£80.00"),
    150: ("Pro Trial", "£150.00"),
    1000: ("Full Access", "£1000.00"),
}

MENU_FOOTER = (
    "Nebula AI is now ready to start your first automated trading session. "
    "Please choose an option from the menu below"
)


def account_summary(account_id: str, amount: int) -> str:
    """The account block shared by the activation message and the main menu."""
    plan, balance = PLANS.get(amount, ("Full Access", f"£{amount}.00"))
    return (
        f"Account ID: {account_id}\n"
        f"Access Plan: {plan}\n"
        f"Start Balance: {balance}\n"
        "Status: Active"
    )


# Shared header for every plan; only the details block below changes.
SESSION_HEADER = (
    "Your Nebula AI trading module is ready \n\n"
    "Before starting, the system will analyse the market, select suitable assets "
    "and prepare the trading strategy based on your access plan\n\n"
    "<b>Session details:</b>\n"
)

SESSION_DETAILS: dict[int, str] = {
    80: (
        "Access Plan: Starter Trial\n"
        "Trading Sessions: 1 available\n"
        "Expected profit per session: up to £2,500\n"
        "Active Trading Time: up to 3 hours\n"
        "Mode: AI Automated Trading"
    ),
    150: (
        "Access Plan: Pro Trial\n"
        "Trading Sessions: 2 available\n"
        "Expected profit per session: up to £4,000\n"
        "Active Trading Time: up to 5 hours\n"
        "Mode: AI Automated Trading"
    ),
    1000: (
        "Access Plan: Full Access\n"
        "Trading Sessions: Unlimited \n"
        "Expected profit: up to £65,000/month\n"
        "Active Trading Time: Unlimited\n"
        "Mode: AI Automated Trading"
    ),
}

# Shown in Trading History before the user has started a session.
NO_HISTORY_TEXT = (
    "<b>No trading sessions found.</b>\n\n"
    "You haven’t started any trading sessions yet.\n"
    "Once Nebula AI completes your first trade, all trading reports will appear here\n\n"
    "To begin, start your first trading session"
)

TRADE_HISTORY: dict[int, str] = {
    80: (
        "<b>Successful Trades:</b> 4\n\n"
        "✅ <b>Trade 1</b> — BTC/USDT\n"
        "<b>Direction:</b> SHORT\n"
        "<b>Start:</b> £80.00\n"
        "<b>Close:</b> £200.81\n"
        "<b>Profit:</b> +£120.81\n\n"
        "✅ <b>Trade 2</b> — SOL/USDT\n"
        "<b>Direction:</b> LONG\n"
        "<b>Start:</b> £200.81\n"
        "<b>Close:</b> £479.45\n"
        "<b>Profit:</b> +£278.64\n\n"
        "✅ <b>Trade 3</b> — ETH/USDT\n"
        "<b>Direction:</b> LONG\n"
        "<b>Start:</b> £479.45\n"
        "<b>Close:</b> £1,109.93\n"
        "<b>Profit:</b> +£630.48\n\n"
        "✅ <b>Trade 4</b> — LTC/USDT\n"
        "<b>Direction:</b> SHORT\n"
        "<b>Start:</b> £1,109.93\n"
        "<b>Close:</b> £2,488.80\n"
        "<b>Profit:</b> +£1,378.87"
    ),
    150: (
        "<b>Successful Trades:</b> 4\n\n"
        "✅ <b>Trade 1</b> — BTC/USDT\n"
        "<b>Direction:</b> SHORT\n"
        "<b>Start:</b> £150.00\n"
        "<b>Close:</b> £398.76\n"
        "<b>Profit:</b> +£248.76\n\n"
        "✅ <b>Trade 2</b> — SOL/USDT\n"
        "<b>Direction:</b> LONG\n"
        "<b>Start:</b> £398.76\n"
        "<b>Close:</b> £993.99\n"
        "<b>Profit:</b> +£595.23\n\n"
        "✅ <b>Trade 3</b> — ETH/USDT\n"
        "<b>Direction:</b> LONG\n"
        "<b>Start:</b> £993.99\n"
        "<b>Close:</b> £2,297.91\n"
        "<b>Profit:</b> +£1,303.92\n\n"
        "✅ <b>Trade 4</b> — LTC/USDT\n"
        "<b>Direction:</b> SHORT\n"
        "<b>Start:</b> £2,297.91\n"
        "<b>Close:</b> £4,987.76\n"
        "<b>Profit:</b> +£2,689.85"
    ),
    1000: (
        "<b>Successful Trades:</b> 4\n\n"
        "✅ <b>Trade 1</b> — BTC/USDT\n"
        "<b>Direction:</b> SHORT\n"
        "<b>Start:</b> £1,000.00\n"
        "<b>Close:</b> £2,184.30\n"
        "<b>Profit:</b> +£1,184.30\n\n"
        "✅ <b>Trade 2</b> — SOL/USDT\n"
        "<b>Direction:</b> LONG\n"
        "<b>Start:</b> £2,184.30\n"
        "<b>Close:</b> £4,471.70\n"
        "<b>Profit:</b> +£2,287.40\n\n"
        "✅ <b>Trade 3</b> — ETH/USDT\n"
        "<b>Direction:</b> LONG\n"
        "<b>Start:</b> £4,471.70\n"
        "<b>Close:</b> £8,656.32\n"
        "<b>Profit:</b> +£4,184.62\n\n"
        "✅ <b>Trade 4</b> — LTC/USDT\n"
        "<b>Direction:</b> SHORT\n"
        "<b>Start:</b> £8,656.32\n"
        "<b>Close:</b> £15,678.42\n"
        "<b>Profit:</b> +£7,022.10"
    ),
}


# Minimum withdrawal threshold shown per plan before a session has been started.
WITHDRAW_MIN: dict[int, str] = {
    80: "£1,000.00",
    150: "£2,000.00",
    1000: "£3,500.00",
}


def no_withdraw_text(amount: int) -> str:
    """Shown when the user taps Withdraw before starting a session."""
    min_amount = WITHDRAW_MIN.get(amount, WITHDRAW_MIN[1000])
    _, balance = PLANS.get(amount, ("Full Access", f"£{amount}.00"))
    return (
        "<b>Withdrawal is not available yet.</b>\n\n"
        f"📤  Minimum withdrawal amount: <b>{min_amount}</b>\n"
        f"💰 Your current balance: <b>{balance}</b>\n"
        " \n"
        "You don’t have enough funds available for withdrawal yet. "
        "Start a trading session first to increase your available balance"
    )


# Balance available for withdrawal after a session — the closing figure of each
# plan's final trade in TRADE_HISTORY.
WITHDRAW_BALANCE: dict[int, str] = {
    80: "£2,488.80",
    150: "£4,987.76",
    1000: "£15,678.42",
}


def withdraw_available_text(amount: int) -> str:
    """Shown when the user taps Withdraw after a session has been used."""
    min_amount = WITHDRAW_MIN.get(amount, WITHDRAW_MIN[1000])
    balance = WITHDRAW_BALANCE.get(amount, WITHDRAW_BALANCE[1000])
    # The Full Access plan skips the "funds are available" header line.
    return (
        f"<b>Your funds are available for withdrawal.</b>\n\n"
        f"<b>📤  Minimum withdrawal amount: {min_amount}</b>\n"
        f"💰 Your current balance: <b>{balance}</b>\n\n"
        "Please choose your preferred withdrawal method below"
    )


# Prompt shown after the user picks the IBAN withdrawal method.
IBAN_PROMPT_TEXT = (
    "<b>🏦 Withdraw to IBAN</b>\n\n"
    "Please enter your bank IBAN below\n\n"
    "<i>Make sure the details are correct before continuing. "
    "Incorrect bank details may delay the withdrawal process</i>"
)

# Prompt shown after the user picks the CRYPTO withdrawal method.
CRYPTO_PROMPT_TEXT = (
    "<b>🌐 Withdraw to CRYPTO</b>\n\n"
    "Please enter your cryptocurrency wallet address below\n\n"
    "<i>Make sure the wallet address and network are correct before continuing. "
    "Incorrect crypto details may delay or prevent the withdrawal</i>"
)

# Method id -> its input prompt. Also used to know the label in the confirmation.
WITHDRAW_PROMPTS: dict[str, str] = {
    "IBAN": IBAN_PROMPT_TEXT,
    "CRYPTO": CRYPTO_PROMPT_TEXT,
}


def confirm_withdraw_text(amount: int, method: str, destination: str) -> str:
    """Confirmation screen shown once the user has entered their destination."""
    balance = WITHDRAW_BALANCE.get(amount, WITHDRAW_BALANCE[1000])
    return (
        "<b>📤 Confirm Withdrawal</b>\n\n"
        "You are about to withdraw your available funds.\n\n"
        f"<b>Withdrawal Amount:</b> {balance}\n"
        f"<b>Method:</b> {method}\n"
        f"<b>Destination:</b> {destination}\n\n"
        "Please confirm that all details are correct. "
        "This action cannot be cancelled after confirmation\n\n"
        "<i>⏳ Payment processing may take from <b>15 minutes to 3 hours</b></i>"
    )


async def _render_main_menu(message: Message, repo: Repo):
    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    account_id = user.account_id if user and user.account_id else "—"
    amount = user.amount if user and user.amount else 80
    keyboard = post_session_kb() if user and user.session_used else main_menu_kb()
    return account_summary(account_id, amount) + "\n\n" + MENU_FOOTER, keyboard


async def _render_session(message: Message, repo: Repo):
    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    amount = user.amount if user and user.amount else 80
    details = SESSION_DETAILS.get(amount, SESSION_DETAILS[1000])
    return SESSION_HEADER + details, session_kb()


async def _render_history(message: Message, repo: Repo):
    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    if not user or not user.session_used:
        return NO_HISTORY_TEXT, back_kb()
    amount = user.amount if user.amount in TRADE_HISTORY else 80
    return TRADE_HISTORY[amount], back_kb()


async def _render_withdraw(message: Message, repo: Repo):
    user = await repo.user.get_user_by_id(message.from_user.id)  # type: ignore
    amount = user.amount if user and user.amount else 80
    if user and user.session_used:
        # Post-session: funds are unlocked; offer the withdrawal methods.
        return withdraw_available_text(amount), withdraw_method_kb()
    # Pre-session: withdrawal is locked and we show the minimum-threshold notice.
    return no_withdraw_text(amount), back_kb()


# Registry: screen id -> async render(message, repo) -> (text, keyboard)
SCREENS = {
    MAIN_MENU: _render_main_menu,
    SESSION: _render_session,
    HISTORY: _render_history,
    WITHDRAW: _render_withdraw,
}


async def _get_stack(state: FSMContext) -> list[str]:
    data = await state.get_data()
    return list(data.get("nav_stack", [MAIN_MENU]))


async def show_screen(
    message: Message, state: FSMContext, repo: Repo, screen: str, *, push: bool = True
) -> None:
    """Render a screen; by default push it onto the navigation stack."""
    if push:
        stack = await _get_stack(state)
        stack.append(screen)
        await state.update_data(nav_stack=stack)
    text, keyboard = await SCREENS[screen](message, repo)
    await message.answer(text, reply_markup=keyboard)


async def go_back(message: Message, state: FSMContext, repo: Repo) -> None:
    """Pop the current screen and re-render the previous one."""
    stack = await _get_stack(state)
    if len(stack) > 1:
        stack.pop()
    await state.update_data(nav_stack=stack)
    await show_screen(message, state, repo, stack[-1], push=False)
