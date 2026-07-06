from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

AMOUNTS = (80, 150, 1000)


def admin_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Generate Key")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def amounts_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for amount in AMOUNTS:
        builder.button(text=f"{amount}£")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
