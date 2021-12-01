from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderStates(StatesGroup):

    # States
    song = State()
    congratulation = State()
    approve = State()
