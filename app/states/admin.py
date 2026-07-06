from aiogram.fsm.state import State, StatesGroup


class GenerateKey(StatesGroup):
    amount = State()
