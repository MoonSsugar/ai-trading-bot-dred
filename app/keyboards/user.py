from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Button labels (kept as constants so handlers match on the exact text).
BTN_START_TRADING = "🚀 Start Trading Session"
BTN_HISTORY = "📊 Trading History"
BTN_WITHDRAW = "💸 Withdraw Funds"
BTN_HELP = "🛟 Help"

BTN_CONTACT_MANAGER = "👤 Contact Your Trading Manager"
MANAGER_URL = "https://t.me/RobertNebulaAI"

BTN_START_SESSION = "🚀 Start Session"
BTN_BACK = "⬅️ Back"

BTN_IBAN = "🏦  IBAN"
BTN_CRYPTO = "🌐 Crypto"

BTN_WITHDRAW_CONFIRM = "✅ Withdraw funds"


def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_START_TRADING)
    builder.button(text=BTN_HISTORY)
    builder.button(text=BTN_WITHDRAW)
    builder.button(text=BTN_HELP)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def session_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_START_SESSION)
    builder.button(text=BTN_BACK)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def withdraw_method_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_IBAN)
    builder.button(text=BTN_CRYPTO)
    builder.button(text=BTN_BACK)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def confirm_withdraw_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_WITHDRAW_CONFIRM)
    builder.button(text=BTN_BACK)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def back_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_BACK)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


# Callback ids for the inline menu shown on the suspension image.
CB_SUSPENDED_HISTORY = "wsm:history"
CB_SUSPENDED_WITHDRAW = "wsm:withdraw"
CB_SUSPENDED_HELP = "wsm:help"
CB_SUSPENDED_CLOSE = "wsm:close"


def suspended_menu_kb() -> InlineKeyboardMarkup:
    # Inline (not reply) because "Contact Manager" must open a t.me URL, which
    # only inline keyboards support.
    builder = InlineKeyboardBuilder()
    builder.button(text=BTN_CONTACT_MANAGER, url=MANAGER_URL)
    builder.button(text=BTN_HISTORY, callback_data=CB_SUSPENDED_HISTORY)
    builder.button(text=BTN_WITHDRAW, callback_data=CB_SUSPENDED_WITHDRAW)
    builder.button(text=BTN_HELP, callback_data=CB_SUSPENDED_HELP)
    builder.adjust(1)
    return builder.as_markup()


def suspended_back_kb() -> InlineKeyboardMarkup:
    # Back button for the sub-screens opened from the suspension menu.
    builder = InlineKeyboardBuilder()
    builder.button(text=BTN_BACK, callback_data=CB_SUSPENDED_CLOSE)
    builder.adjust(1)
    return builder.as_markup()


def post_session_kb() -> ReplyKeyboardMarkup:
    # Same as the main menu but without "Start Trading Session": once a session
    # has run, the user cannot start another one.
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_HISTORY)
    builder.button(text=BTN_WITHDRAW)
    builder.button(text=BTN_HELP)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
