from aiogram.fsm.state import State, StatesGroup


class Activation(StatesGroup):
    # Set while we expect the user to type their activation code.
    code = State()


class Withdraw(StatesGroup):
    # Waiting for the user to type their destination (IBAN or crypto address).
    address = State()
    # Showing the confirmation screen, waiting for confirm/back.
    confirm = State()
