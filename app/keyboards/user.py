from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Button labels (kept as constants so handlers match on the exact text).
BTN_START_TRADING = "🚀 Start Trading Session"
BTN_HISTORY = "📊 Trading History"
BTN_WITHDRAW = "💸 Withdraw Funds"
BTN_HELP = "🛟 Help"

BTN_START_SESSION = "🚀 Start Session"
BTN_BACK = "⬅️ Back"


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


def back_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_BACK)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def post_session_kb() -> ReplyKeyboardMarkup:
    # Same as the main menu but without "Start Trading Session": once a session
    # has run, the user cannot start another one.
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_HISTORY)
    builder.button(text=BTN_WITHDRAW)
    builder.button(text=BTN_HELP)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
