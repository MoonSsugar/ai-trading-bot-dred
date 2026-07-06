from aiogram.fsm.state import State, StatesGroup


class Activation(StatesGroup):
    # Set while we expect the user to type their activation code.
    code = State()
